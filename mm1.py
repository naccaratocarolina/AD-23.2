import numpy as np

BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
ORANGE = '\033[33m'
END = '\033[0m'

class Event:
  def __init__(self, type, timestamp, id):
    self.type = type
    self.timestamp = timestamp
    self.id = id

  def __str__(self):
    return f'{self.type} {self.id} {self.timestamp:.2f}'

def generate_next_arrival(arrival_rate):
  return np.random.exponential(1/arrival_rate)

def generate_next_departure(service_rate):
  return np.random.exponential(1/service_rate)

def print_queue(queue):
  return f'[{", ".join([str(event) for event in queue])}]'

def mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len):
  queue = []
  clock = 0
  N = 0
  customer_number = 0

  def schedule_event(type, timestamp):
    nonlocal customer_number
    event = Event(type, timestamp, customer_number)
    queue.append(event)
    print_queue(queue)
    queue.sort(key=lambda x: x.timestamp)
    customer_number += 1

  # Simulação começa com chegada de cliente
  schedule_event('Arrival', generate_next_arrival(arrival_rate))

  is_busy = True
  while True:
    if len(queue) == 0:
      break

    event = queue.pop(0)
    clock = event.timestamp

    # Handler de chegada
    if event.type == 'Arrival':
      if max_queue_len == -1 or N < max_queue_len:
        schedule_event('Arrival', clock + generate_next_arrival(arrival_rate))
        N += 1
        print(f'{GREEN}{clock:.2f}: Cliente chega (N = {N}){END}')
        if N == 1:
          schedule_event('Departure', clock + generate_next_departure(service_rate))
      else:
        print(f'{RED}{clock:.2f}: Cliente desiste (N = {N}){END}')

    # Handler de partida
    if event.type == 'Departure':
      if N > 0:
        if not is_busy:
          print(f'{CYAN}{clock:.2f}: Servidor volta a atender (N = {N}){END}')
        N -= 1
        is_busy = True
        schedule_event('Departure', clock + generate_next_departure(service_rate))
        print(f'{YELLOW}{clock:.2f}: Cliente parte (N = {N}){END}')

    if N == 0 and is_busy:
      print(f'{BLUE}{clock:.2f}: Servidor ocioso (N = {N}){END}')
      is_busy = False

    max_iter -= 1

    # Condição de parada
    # if N == 0:
    if max_iter == 0:
        break

def generate_next_event(probability, timestamp):
  if np.random.rand() < probability:
    return Event('Win', timestamp, 1)
  else:
    return Event('Lose', timestamp, -1)

def gambler_ruin(probability, goal, starting_amount):
  clock = 0
  amount = starting_amount

  while amount > 0 and amount < goal:
    event = generate_next_event(probability, clock)
    clock += 1
    amount += event.id
    if event.type == 'Win':
      print(f'{PURPLE}{clock}: Jogador ganhou {event.id} | Montante Atual: {amount}{END}')
    else:
      print(f'{BLUE}{clock}: Jogador perdeu {event.id*-1} | Montante: {amount}{END}')

  if amount == goal:
    print(f'O apostador atingiu o objetivo de {goal} em {clock} rodadas')
  else:
    print(f'O apostador faliu em {clock} rodadas')

def main():
  arrival_rate = 1
  service_rate = 2
  max_iter = 10
  max_queue_len = 5

  mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len)

  print()
  
  win_probability = 0.5
  goal = 10
  starting_amount = 1
  gambler_ruin(win_probability, goal, starting_amount)

if __name__ == '__main__':
  main()
