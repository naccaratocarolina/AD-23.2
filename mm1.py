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
      return f'{self.type} {self.id}'

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
  server_busy = False

  def schedule_event(type, time):
    nonlocal customer_number
    event = Event(type, time, customer_number)
    queue.append(event)
    print_queue(queue)
    queue.sort(key=lambda x: x.time)
    customer_number += 1

  schedule_event('Arrival', generate_next_arrival(arrival_rate))
  is_busy = True
  while True:
    event = queue.pop(0)
    clock = event.time

    if event.type == 'Arrival':
        schedule_event('Arrival', clock + generate_next_arrival(arrival_rate))
        N += 1
        print(f"{GREEN}{clock:.2f}: Cliente #{event.id} chega (N = {N}) {print_queue(queue)}{END}")
        if N == 1:
            schedule_event('Departure', clock + generate_next_departure(service_rate))

    if event.type == 'Departure':
      if N > 0:
        if not is_busy:
          print(f'{BLUE}{clock:.2f}: Servidor volta a ficar ocupado (N = {N}){END}')
        N -= 1
        is_busy = True
        schedule_event('Departure', clock + generate_next_departure(service_rate))
        print(f"{ORANGE}{clock:.2f}: Cliente #{event.id} parte (N = {N}) {print_queue(queue)}{END}")

    if N == 0 and is_busy:
      print(f"{BLUE}{clock:.2f}: Servidor ocioso (N = {N}) {print_queue(queue)}{END}")
      is_busy = False

    max_iter -= 1
    if max_iter == 0:
        break

def main():
  arrival_rate = 1
  service_rate = 1
  max_iter = 20
  max_queue_len = 3

  mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len)

if __name__ == '__main__':
  main()
