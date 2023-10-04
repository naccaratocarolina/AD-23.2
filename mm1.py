import numpy as np

class Event:
  def __init__(self, event_type, time):
    self.event_type = event_type
    self.time = time

def generate_next_arrival(arrival_rate):
  return np.random.exponential(1/arrival_rate)

def generate_next_departure(service_rate):
  return np.random.exponential(1/service_rate)

def mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len):
  queue = []
  clock = 0
  N = 0

  def schedule_event(event_type, time):
    event = Event(event_type, time)
    queue.append(event)
    queue.sort(key=lambda x: x.time)

  print(f"{clock:.2f}: Iniciando simulacao")
  schedule_event("arrival", generate_next_arrival(arrival_rate))

  while max_iter > 0:
    event = queue.pop(0)
    clock += event.time
    is_idle = (N == 0)

    if event.event_type == "arrival":
      print(f"{clock:.2f}: Cliente chega (N = {N + 1}) {event.time:.2f}")
      schedule_event("arrival", clock + generate_next_arrival(arrival_rate))

      N += 1
      if N == 1:
        schedule_event("service", clock + generate_next_departure(service_rate))
        
    if event.event_type == "service":
      print(f"{clock:.2f}: Cliente parte (N = {N - 1}) {event.time:.2f}")
      N -= 1
      if N > 0:
        schedule_event("service", clock + generate_next_departure(service_rate))
    
    if is_idle:
      print(f"{clock:.2f}: Servidor ocioso")
    max_iter -= 1

def main():
  arrival_rate = 0.5
  service_rate = 0.6
  max_iter = 10
  max_queue_len = 10

  mm1_simulation(arrival_rate, service_rate, max_iter, max_queue_len)

if __name__ == '__main__':
  main()