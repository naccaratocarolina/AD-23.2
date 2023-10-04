import numpy as np

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[93m'
END = '\033[0m'

class Event:
  def __init__(self, type, time, id):
    self.type = type
    self.time = time
    self.id = id

  def __str__(self):
    return f'{self.type} {self.id} {self.time:.2f}'

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

  def schedule_event(type, time):
    nonlocal customer_number
    event = Event(type, time, customer_number)
    queue.append(event)
    print_queue(queue)
    queue.sort(key=lambda x: x.time)
    customer_number += 1

  # Simulação começa com chegada de cliente
  schedule_event('Arrival', generate_next_arrival(arrival_rate))

  is_busy = True
  while True:
    if len(queue) == 0:
      break

    event = queue.pop(0)
    clock = event.time

    # Handler de chegada
    if event.type == 'Arrival':
      if max_queue_len == -1 or N < max_queue_len:
        schedule_event('Arrival', clock + generate_next_arrival(arrival_rate))
        N += 1
        print(f'{GREEN}{clock:.2f}: Cliente #{event.id} chega (N = {N}){END}')
        if N == 1:
          schedule_event('Departure', clock + generate_next_departure(service_rate))
      else:
        print(f'{RED}{clock:.2f}: Cliente #{event.id} desiste (N = {N}){END}')

    # Handler de partida
    if event.type == 'Departure':
      if N > 0:
        if not is_busy:
          print(f'{BLUE}{clock:.2f}: Servidor ocupado novamente (N = {N}){END}')
        N -= 1
        is_busy = True
        schedule_event('Departure', clock + generate_next_departure(service_rate))
        print(f'{ORANGE}{clock:.2f}: Cliente #{event.id} parte (N = {N}){END}')

    if N == 0 and is_busy:
      print(f'{BLUE}{clock:.2f}: Servidor ocioso (N = {N}){END}')
      is_busy = False

    max_iter -= 1

    # Condição de parada
    # if N == 0:
    if max_iter == 0:
        break

def main():
  arrival_rate = 10
  service_rate = 1
  max_iter = 50
  max_queue_len = 5

  mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len)

if __name__ == '__main__':
  main()
