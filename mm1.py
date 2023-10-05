import numpy as np

BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
ORANGE = '\033[33m'
END = '\033[0m'

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

def generate_next_arrival(arrival_rate):
  return np.random.exponential(1/arrival_rate)

def generate_next_departure(service_rate):
  return np.random.exponential(1/service_rate)

def print_queue(L):
  print(f'[{", ".join([str(event) for event in L])}]')

def mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len):
  L = [] # Lista de eventos (Fila de prioridades)
  N = 0 # Número de clientes na fila (variavel de estado)
  clock = 0
  customer_number = 0 

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
  while len(L) > 0 and max_iter > 0:
    e = L.pop(0) # Remove evento e da fila (de prioridades) de eventos
    clock = e.timestamp # Atualiza relógio

    # Sortear tempo da próxima chegada e agendar evento
    # Se N = 1, sortear tempo da próxima partida e agendar partida
    if e.type == 'Arrival':
      if max_queue_len == -1 or N < max_queue_len:
        schedule_event('Arrival', clock + generate_next_arrival(arrival_rate))
        N += 1
        print(f'{GREEN}{clock:.2f}: Cliente chega (N = {N}){END}')
        if N == 1:
          schedule_event('Departure', clock + generate_next_departure(service_rate))
      else:
        print(f'{RED}{clock:.2f}: Cliente desiste (N = {N}){END}')

    # Se N > 0, sortear tempo da próxima partida e agendar partida
    if e.type == 'Departure':
      if N > 0:
        # Se servidor estava ocioso, servidor volta a atender
        if not is_busy:
          print(f'{CYAN}{clock:.2f}: Servidor volta a atender (N = {N}){END}')
        N -= 1
        is_busy = True
        schedule_event('Departure', clock + generate_next_departure(service_rate))
        print(f'{YELLOW}{clock:.2f}: Cliente parte (N = {N}){END}')

    # Se N = 0 e servidor estava ocupado, servidor fica ocioso
    if N == 0 and is_busy:
      print(f'{BLUE}{clock:.2f}: Servidor ocioso (N = {N}){END}')
      is_busy = False

    max_iter -= 1 # Decrementa variável de controle

def mm1(arrival_rate, service_rate, max_iter, max_queue_len, iterations=2):
  counter = 0
  while counter < iterations:
    print(f'{ORANGE}Simulação #{counter+1}{END}')
    mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len)
    print()
    counter += 1
 
# ================================
# Ruína do Apostador
# ================================

def generate_next_event(probability, timestamp):
  if np.random.rand() < probability:
    return Event('Win', timestamp, 1)
  else:
    return Event('Lose', timestamp, -1)

def gambler_ruin(probability, goal, starting_amount):
  amount = starting_amount # Equivalente a primeira chegada
  round = 0 # Número de rodadas ("clock")

  # Plano de controle (enquanto o apostador não atingir o objetivo ou falir)
  while amount > 0 and amount < goal:
    round += 1
    event = generate_next_event(probability, round)
    amount += event.id

    # 
    if event.type == 'Win':
      print(f'{PURPLE}{round}: Jogador ganhou {event.id} | Montante: {amount}{END}')
    
    if event.type == 'Lose':
      print(f'{BLUE}{round}: Jogador perdeu {event.id*-1} | Montante: {amount}{END}')

  # Imprime resultado
  if amount == goal:
    print(f'O apostador atingiu o objetivo de {goal} em {round} rodadas')
  else:
    print(f'O apostador faliu em {round} rodadas')

def gambler(win_probability, goal, starting_amount, iterations=2):
  counter = 0
  while counter < iterations:
    print(f'{ORANGE}Simulação #{counter+1}{END}')
    gambler_ruin(win_probability, goal, starting_amount)
    print()
    counter += 1

def main():
  mm1(0.5, 1, 5, -1, 4)
  print()
  gambler(0.5, 5, 2, 4)

if __name__ == '__main__':
  main()
