import numpy as np
import matplotlib.pyplot as plt

BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
ORANGE = '\033[33m'
BLACK_BG = '\033[40;37m'
END = '\033[0m'


def print_message(msg, color, clock, verbose):
    if verbose:
        clock = round(clock, 2) if clock > -1 else ''
        print(f'{color}{clock} {msg}{END}')


# ================================
# Evento
# ================================
class Event:
    def __init__(self, type, timestamp, id, prev=None, next=None):
        self.type = type
        self.timestamp = timestamp
        self.id = id
        self.prev = prev
        self.next = next

    def set_prev(self, prev):
        self.prev = prev

    def set_next(self, next):
        self.next = next

    def __str__(self):
        prev = f'type={self.prev.type} id={self.prev.id}' if self.prev else 'x'
        next = f'type={self.next.type} id={self.next.id}' if self.next else 'x'
        return f'{self.type} id={self.id} timestamp={self.timestamp:.2f} prev={prev} next={next}'


# ================================
# M/M/1
# ================================
CURRENT_ITERATION = 0


def generate_next_arrival(arrival_rate):
    return np.random.exponential(1 / arrival_rate)


def generate_next_departure(service_rate):
    return np.random.exponential(1 / service_rate)


def print_queue(L):
    print(f'[{", ".join([str(event) for event in L])}]')


def mm1_simulation(arrival_rate, service_rate, max_events=-1, max_queue_len=-1, verbose=True):
    global CURRENT_ITERATION
    CURRENT_ITERATION += 1
    if verbose:
        max_events_str = max_events if max_events > 0 else 'infinito'
        max_queue_len_str = max_queue_len if max_queue_len > 0 else 'infinito'
        print_message(
            f'Chegada: {arrival_rate} | Partida: {service_rate} | Iterações: {max_events_str} | Tamanho máximo da fila: {max_queue_len_str}',
            BLACK_BG, -1, verbose)
    L = []  # Lista de eventos (Fila de prioridades)
    N = 0  # Número de clientes na fila (variavel de estado)
    clock = 0
    customer_number = 0

    # Métricas
    W = 0  # Tempo acumulado de espera na fila
    S = 0  # Tempo acumulado de serviço
    Nt = []  # Lista de tuplas (tempo, N) para cálculo de área sob a curva

    PREV_ARRIVAL = None
    PREV_DEPARTURE = None
    def schedule_event(type, timestamp):
        nonlocal customer_number  # Permite acesso à variável customer_number declarada fora da função
        nonlocal PREV_ARRIVAL, PREV_DEPARTURE
        event = Event(type, timestamp, customer_number)
        L.append(event)  # Adiciona evento
        L.sort(key=lambda x: x.timestamp)  # Ordena fila por prioridade (timestamp)

        # Atualiza referências para eventos anteriores e posteriores
        # As pripriedades prev sempre sao chegadas, e as next sempre sao saidas
        if PREV_ARRIVAL:
            event.set_prev(PREV_ARRIVAL)
        if PREV_DEPARTURE:
            PREV_DEPARTURE.set_next(event)

        customer_number += 1  # Incrementa o número do cliente para o próximo evento

    # Simulação começa com chegada de cliente
    schedule_event('Arrival', generate_next_arrival(arrival_rate))

    # Plano de controle - enquanto a fila não estiver vazia e o número máximo de
    # iterações não for atingido (se max_events = -1, a simulação roda até a fila esvaziar)
    is_busy = True
    while len(L) > 0 and (customer_number < max_events or max_events == -1):
        e = L.pop(0)  # Remove evento e da fila (de prioridades) de eventos
        clock = e.timestamp  # Atualiza relógio

        # Tira uma "foto" do sistema (para estatísticas)
        Nt.append((clock, N))

        # Sortear tempo da próxima chegada e agendar evento
        # Se N = 1, sortear tempo da próxima partida e agendar partida
        if e.type == 'Arrival':
            PREV_ARRIVAL = e

            if max_queue_len == -1 or N < max_queue_len:
                schedule_event( 'Arrival', clock + generate_next_arrival(arrival_rate))
                N += 1
                print_message(f'Cliente chega (N = {N})', GREEN, clock, verbose)
                if N == 1:
                    schedule_event('Departure', clock + generate_next_departure(service_rate))
            else:
                print_message(f'Cliente chega e desiste (N = {N})', RED, clock, verbose)

        # Se N > 0, sortear tempo da próxima partida e agendar partida
        if e.type == 'Departure':
            PREV_DEPARTURE = e

            if N > 0:
                # Atualiza tempo de espera, uma vez que a espera terminou
                wait_time = e.timestamp - e.prev.timestamp
                W += wait_time

                if not is_busy:
                    print_message(f'Servidor volta a atender (N = {N})', CYAN, clock, verbose)

                N -= 1
                is_busy = True

                # Atualiza tempo de serviço e agenda próxima partida
                service_time = generate_next_departure(service_rate)
                S += service_time
                schedule_event('Departure', clock + service_time)
                print_message(f'Cliente sai (N = {N}) Tempo de espera={wait_time:.2f} Tempo de servico={service_time:.2f}', YELLOW, clock, verbose)

        # Se N = 0 e servidor estava ocupado, servidor fica ocioso
        if N == 0 and is_busy:
            print_message(f'Servidor fica ocioso (N = {N})', BLUE, clock, verbose)
            is_busy = False

    stats = {
        'W': W, # Tempo acumulado de espera na fila
        'Wq': W / customer_number, # Tempo médio de espera na fila
        'S': S, # Tempo acumulado de serviço
        'U': S / clock, # Utilização do servidor
        'N': customer_number, # Número de clientes no sistema
        'Nt': Nt, # Lista de tuplas (tempo, N) para cálculo de área
    }
    print(f'W={stats["W"]}')
    print(f'Wq={stats["Wq"]}')
    print(f'S={stats["S"]}')
    print(f'U={stats["U"]}')
    print(f'N={stats["N"]}')
    print(f'Nt={stats["Nt"]}')
    return stats  # Retorna métricas


# ================================
# Ruína do Apostador
# ================================

def generate_next_event(probability, timestamp):
    if np.random.rand() < probability:
        return Event('Win', timestamp, 1)
    else:
        return Event('Lose', timestamp, -1)


def gambler_ruin(probability, goal, starting_amount, verbose=True):
    amount = starting_amount  # Equivalente a primeira chegada
    round = 0  # Número de rodadas ("clock")
    M = []  # (Iteração, Montante)

    # Plano de controle (enquanto o apostador não atingir o objetivo ou falir)
    while amount > 0 and amount < goal:
        round += 1
        event = generate_next_event(probability, round)
        amount += event.id

        M.append((round, amount))

        if event.type == 'Win':
            print_message(f'{round}: Jogador ganhou {event.id} | Montante: {amount}', PURPLE, round, verbose)

        if event.type == 'Lose':
            print_message(f'{round}: Jogador perdeu {event.id} | Montante: {amount}', BLUE, round, verbose)

    # Imprime resultado
    if amount == goal:
        print_message(f'O apostador atingiu o objetivo de {goal} em {round} rodadas', GREEN, round, verbose)
    else:
        print_message(f'O apostador faliu em {round} rodadas', RED, round, verbose)

    return {
        'N': round,
        'Nt': M
    } # Retorna número de rodadas


# ================================
# Estatísticas
# ================================
FONT_SIZE = 12


# Variáveis de interesse:
# Tempo mério de serviço (W) = Tempo médio de um cliente no sistema (fila + servidor)
# Tempo médio de espera na fila (Wq) = Tempo médio de um cliente na fila
# Número médio de clientes no sistema (N) = Média do número de clientes no sistema (fila + servidor)
# Número médio de clientes na fila (Nq) = Média do número de clientes na fila
# Utilização do servidor (U) = Fração de tempo que o servidor está ocupado


# O sistema é simulado por i iterações. Cada iteração possui K clientes.
# Seja W_i_k o tempo de espera do k-ésimo cliente na i-ésima iteração,
# o tempo de espera médio do k-ésimo cliente é W_i = Sum_k W_i_k / K
# Quanto maior K, mais preciso é o resultado
def wait_time(i, func, *args):
    avg_wait_times = []  # Lista com tempos médios de cada iteração i

    for _ in range(i):
        res = func(*args)  # Executa simulação
        total_wait_time = res['W']
        k = res['N']
        avg_wait_time = total_wait_time / k
        avg_wait_times.append(avg_wait_time)

    return avg_wait_times


# Observamos uma execução de simulação. Calculamos a área sob a curva
# da evolução do número de clientes no sistema (N) em função do tempo.
# Para isso, é tirada uma "foto" do sistema a cada iteração, contendo
# uma lista de tuplas no formato (tempo, N)
def area(values):
    area_values = []
    area = 0  # Área acumulada sob a curva
    t_prev, N_prev = 0, 0  # Valores anteriores de tempo e N (inicial = 0)

    for t, N in values:
        area += (t - t_prev) * N_prev  # Calcula área do retângulo
        area_values.append(area)
        t_prev, N_prev = t, N

    return area_values


def plot_area(func, *args, title='Não Definido', xlabel='Não Definido', ylabel='Não Definido', color='black'):
    global FONT_SIZE
    res = func(*args)
    A = res['Nt']
    area_values = area(A)

    fig, ax = plt.subplots(figsize=(6, 4))

    # Listas de coordenadas x e y para plotagem
    x = list(range(len(area_values)))
    y = [0] + area_values

    plt.plot(area_values, color=color, drawstyle='steps-post')
    plt.title(title, fontsize=FONT_SIZE * 1.1)
    plt.xlabel(xlabel, fontsize=FONT_SIZE)
    plt.ylabel(ylabel, fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.grid(True)
    plt.show()


def plot_n_by_time(func, *args, title='Não Definido', xlabel='Não Definido', ylabel='Não Definido', color='black'):
    global FONT_SIZE
    res = func(*args)
    Nt = res['Nt']

    if len(Nt) <= 1:
        return

    t, N = zip(*Nt)
    plt.figure(figsize=(6, 4))
    plt.plot(N, drawstyle='steps-post', color=color)

    mean_N = [sum(N[:i + 1]) / (i + 1) for i in range(len(N))]
    plt.plot(mean_N, color='crimson', linestyle='--', label='E[Nt]')

    plt.title(title, fontsize=FONT_SIZE * 1.1)
    plt.xlabel(xlabel, fontsize=FONT_SIZE)
    plt.ylabel(ylabel, fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.grid(True)
    plt.show()


def plot_mm1(arrival_rate, service_rate, max_events, max_queue_len=-1, verbose=False):
    plot_n_by_time(
        mm1_simulation,
        arrival_rate, service_rate, max_events, max_queue_len, verbose,
        title='Evolução do número de clientes no sistema',
        xlabel='Tempo',
        ylabel='N(t)',
        color='navy'
    )


def plot_gambler(probability, goal, starting_amount=1, verbose=False):
    plot_n_by_time(
        gambler_ruin,
        probability, goal, starting_amount, verbose,
        title='Evolução do montante do apostador',
        xlabel='Rodada',
        ylabel='Montante',
        color='purple'
    )
def main():
    # np.random.seed(43)
    plot_mm1(0.5, 0.5, 100)
    plot_gambler(0.5, 10, verbose=True)
    mm1_simulation(0.5, 0.5, 10, 10, True)


if __name__ == '__main__':
    main()
