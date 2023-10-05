import numpy as np
import matplotlib.pyplot as plt
import math

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
  def __init__(self, type, timestamp, id):
    self.type = type 
    self.timestamp = timestamp
    self.id = id

  def __str__(self):
    return f'{self.type} {self.id} {self.timestamp:.2f}'

# ================================
# M/M/1
# ================================
CURRENT_ITERATION = 0

def generate_next_arrival(arrival_rate):
  return np.random.exponential(1/arrival_rate)

def generate_next_departure(service_rate):
  return np.random.exponential(1/service_rate)

def print_queue(L):
  print(f'[{", ".join([str(event) for event in L])}]')

def mm1_simulation(arrival_rate, service_rate, max_events, max_queue_len, verbose=True):
  print_message(f'Iteração #{CURRENT_ITERATION}', BLACK_BG, -1, verbose)
  print_message(f'Chegada: {arrival_rate} | Partida: {service_rate} | Iterações: {max_events} | Tamanho máximo da fila: {max_queue_len}', BLACK_BG, -1, verbose)
  L = [] # Lista de eventos (Fila de prioridades)
  N = 0 # Número de clientes na fila (variavel de estado)
  clock = 0
  customer_number = 0 
  total_wait_time = 0 # Métrica importante para estatísticas
  # Variáveis auxiliares para calcular secundárias:
  #   tempo de espera médio, tempo de serviço médio, tempo de resposta médio,
  #   taxa de utilização do servidor
  N_list = [] # Lista de número de clientes na fila a cada evento
  clock_list = [] # Lista de tempos de cada evento
  wait_time_list = [] # Lista de tempos de espera de cada evento
  mean_N = [] # Lista de médias do núm de clientes na fila a cada evento
  mean_clocks = [] # Lista de médias dos tempos de cada evento
  mean_wait_times = [] # Lista de médias dos tempos de espera de cada evento
  meanN = 0 # Média do número de clientes na fila
  meanClock = 0 # Média do tempo de cada evento
  meanWaitTime = 0 # Média do tempo de espera de cada evento

  def schedule_event(type, timestamp):
    nonlocal customer_number  # Permite acesso à variável customer_number declarada fora da função
    event = Event(type, timestamp, customer_number)
    L.append(event) # Adiciona evento
    L.sort(key=lambda x: x.timestamp) # Ordena fila por prioridade (timestamp)
    customer_number += 1  # Incrementa o número do cliente para o próximo evento

  # Simulação começa com chegada de cliente
  schedule_event('Arrival', generate_next_arrival(arrival_rate))

  # Plano de controle (enquanto a fila não estiver vazia e o número máximo de
  # iterações não for atingido)
  is_busy = True
  while len(L) > 0 and max_events > 0:
    e = L.pop(0) # Remove evento e da fila (de prioridades) de eventos
    wait_time = e.timestamp - clock # Calcula tempo de espera
    clock = e.timestamp # Atualiza relógio

    # Sortear tempo da próxima chegada e agendar evento
    # Se N = 1, sortear tempo da próxima partida e agendar partida
    if e.type == 'Arrival':
      if max_queue_len == -1 or N < max_queue_len:
        schedule_event('Arrival', clock + generate_next_arrival(arrival_rate))
        N += 1
        print_message(f'Cliente chega (N = {N})', GREEN, clock, verbose)
        if N == 1:
          schedule_event('Departure', clock + generate_next_departure(service_rate))
      else:
        print_message(f'Cliente chega e desiste (N = {N})', RED, clock, verbose)

    # Se N > 0, sortear tempo da próxima partida e agendar partida
    if e.type == 'Departure':
      if N > 0:
        total_wait_time += wait_time # Atualiza métrica
        # Se servidor estava ocioso, servidor volta a atender
        if not is_busy:
          print_message(f'Servidor volta a atender (N = {N})', CYAN, clock, verbose)
        N -= 1
        is_busy = True
        schedule_event('Departure', clock + generate_next_departure(service_rate))
        print_message(f'Cliente sai (N = {N})', YELLOW, clock, verbose)

    # Se N = 0 e servidor estava ocupado, servidor fica ocioso
    if N == 0 and is_busy:
      print_message(f'Servidor fica ocioso (N = {N})', BLUE, clock, verbose)
      is_busy = False

    max_events -= 1 # Decrementa variável de controle

    # Calcula as métricas adicionais
    if (len(N_list) > 0 and len(clock_list) > 0):
      meanN += N_list[-1] * (clock - clock_list[-1])
      meanClock += (clock - clock_list[-1]) * len(N_list)
      meanWaitTime += wait_time_list[-1] * len(N_list)
    N_list.append(N)
    clock_list.append(clock)
    wait_time_list.append(wait_time)
    mean_N.append(meanN / clock if clock > 0 else 0)
    mean_clocks.append(meanClock / N if N > 0 else 0)
    mean_wait_times.append(meanWaitTime / N if N > 0 else 0)
  
  print()
  metrics = {
    'N': N_list,
    'Clock': clock_list,
    'WaitTime': wait_time_list,
    'MeanN': mean_N,
    'MeanClock': mean_clocks,
    'MeanWaitTime': mean_wait_times
  }
  return total_wait_time, customer_number, metrics # Retorna métrica e número de clientes
 
# ================================
# Ruína do Apostador
# ================================

def generate_next_event(probability, timestamp):
  if np.random.rand() < probability:
    return Event('Win', timestamp, 1)
  else:
    return Event('Lose', timestamp, -1)

def gambler_ruin(probability, goal, starting_amount, verbose=True):
  amount = starting_amount # Equivalente a primeira chegada
  round = 0 # Número de rodadas ("clock")

  # Plano de controle (enquanto o apostador não atingir o objetivo ou falir)
  while amount > 0 and amount < goal:
    round += 1
    event = generate_next_event(probability, round)
    amount += event.id

    if event.type == 'Win':
      print_message(f'{round}: Jogador ganhou {event.id} | Montante: {amount}', PURPLE, round, verbose)
    
    if event.type == 'Lose':
      print_message(f'{round}: Jogador perdeu {event.id} | Montante: {amount}', BLUE, round, verbose)

  # Imprime resultado
  if amount == goal:
    print_message(f'O apostador atingiu o objetivo de {goal} em {round} rodadas', GREEN, round, verbose)
  else:
    print_message(f'O apostador faliu em {round} rodadas', RED, round, verbose)
  
  return round # Retorna número de rodadas

def gambler(win_probability, goal, starting_amount, i=2):
  counter = 0
  while counter < i:
    print(f'{PURPLE}Simulação #{counter+1}{END}')
    gambler_ruin(win_probability, goal, starting_amount)
    print()
    counter += 1

# ================================
# Estatísticas
# ================================

# O sistema é simulado por i iterações. Cada iteração possui K clientes.
# Seja W_i_k o tempo de espera do k-ésimo cliente na i-ésima iteração,
# o tempo de espera médio do k-ésimo cliente é W_i = Sum_k W_i_k / K
# Quanto maior K, mais preciso é o resultado
def wait_time(i, func, *args):
  avg_wait_times = [] # Lista com tempos médios de cada iteração i
  
  for curr in range(i):
    global CURRENT_ITERATION
    CURRENT_ITERATION = curr + 1
    total_wait_time, k, metrics = func(*args) # Executa simulação
    avg_wait_time = total_wait_time / k
    avg_wait_times.append(avg_wait_time)
  
  return avg_wait_times, metrics

def plotGraph(Ns, clocks, meanNs, meanCs, meanTs):
  fig, ax = plt.subplots(figsize=(16,4))
  fig, bx = plt.subplots(figsize=(16,4))
  fig, cx = plt.subplots(figsize=(16,4))
  NsInt = range(min(Ns), math.ceil(max(Ns)) + 1)
  ax.set_yticks(NsInt)
  # Plot the Ns data
  ax.plot(clocks[:-1], Ns[:-1], drawstyle="steps-post", label="N")
  # Plot the meanNs data
  ax.plot(clocks[:-1], meanNs[:-1], linestyle="dashed", label="E[N]")
  # Plot the meanCs data
  bx.plot(clocks[:-1], meanCs[:-1], label="E[C]")
  # Plot the meanTs data
  cx.plot(clocks[:-1], meanTs[:-1], label="E[T]")
  # Plot das labels
  ax.set_xlabel("Clock")
  bx.set_xlabel("Clock")
  cx.set_xlabel("Clock")
  ax.set_ylabel("N")
  bx.set_ylabel("Tempo médio de espera (E[C])")
  cx.set_ylabel("Tempo médio de espera (E[T])")
  ax.set_title("Número de clientes (N) na fila versus Clock")
  bx.set_title("Tempo médio de espera (E[C]) versus Clock")
  cx.set_title("Tempo médio de espera (E[T]) versus Clock")
  # Add a legend
  ax.legend()
  bx.legend()
  cx.legend()
  # Plot
  plt.show()

def main():
  avg_wait_times, metrics = wait_time(10, mm1_simulation, 0.5, 1, 10, -1, True)
  print(avg_wait_times)
  plotGraph(metrics['N'], metrics['Clock'], metrics['MeanN'], metrics['MeanClock'], metrics['MeanWaitTime'])
  # mm1(0.5, 1, 10, -1, 1)
  # print()
  # gambler(0.5, 5, 2, 4)

if __name__ == '__main__':
  main()
