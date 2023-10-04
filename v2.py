import numpy as np
from utils import *

ARRIVAL_COLOR = '\033[93m' # Amarelo
DEPARTURE_COLOR = '\033[94m' # Azul
END_COLOR = '\033[0m' # Branco

LAST_ARRIVAL = 0

# Eventos da simulação de fila M/M/1
class Arrival(Event):
  def __init__(self, arrival_rate, clock):
    self.arrival_rate = arrival_rate
    self.next_arrival = self.generate_next_arrival(arrival_rate)
    self.priority = clock + self.next_arrival
    self.clock = clock
    super().__init__('Chegada', self.priority)
  
  def generate_next_arrival(self, arrival_rate):
    return np.random.exponential(1/arrival_rate)
  
  def next(self):
    return self.next_arrival
  
  def interarrival(self):
    return self.clock - LAST_ARRIVAL
  
  def __str__(self):
    print(self.interarrival())
    return f'{self.type} {self.next_arrival:.2f}'

class Departure(Event):
  def __init__(self, service_rate, clock):
    self.service_rate = service_rate
    self.next_departure = self.generate_next_departure(service_rate)
    self.priority = clock + self.next_departure
    super().__init__('Partida', self.priority)
  
  def generate_next_departure(self, service_rate):
    return np.random.exponential(1/service_rate)
  
  def next(self):
    return self.next_departure
  
  def __str__(self):
    return f'{self.type} Tempo de serviço {self.next_departure:.2f}'

# Simulação de fila M/M/1
class MM1Simulation(Simulation):
  def __init__(self, arrival_rate, service_rate, max_time, max_size):
    self.sort = min
    super().__init__(max_time, max_size, self.sort)
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
    self.next_arrival = float('inf')
    self.next_departure = float('inf')
  
  def generate_arrival(self):
    return Arrival(self.arrival_rate, self.clock)
  
  def generate_departure(self):
    return Departure(self.service_rate, self.clock)
  
  def arrival(self):
    global LAST_ARRIVAL
    if not self.events.isFull():
      next_arrival = self.generate_arrival()
      self.next_arrival = next_arrival.next()
      self.clock += self.next_arrival
      self.schedule_event(next_arrival)
      LAST_ARRIVAL = self.clock
      print(f'{self.clock:.2f}: {ARRIVAL_COLOR}{next_arrival}{END_COLOR}')
    else:
      print(f'{self.clock:.2f}: {ARRIVAL_COLOR}Chegada bloqueada{END_COLOR}')
  
  def departure(self):
    next_departure = self.generate_departure()
    self.next_departure = next_departure.next()
    self.clock += self.next_departure
    self.schedule_event(next_departure)
    print(f'{self.clock:.2f}: {DEPARTURE_COLOR}{next_departure}{END_COLOR}')
    return next_departure
  
  def process_event(self, event):
    if event.type == 'Chegada':
      if self.next_departure == float('inf'):
        self.departure()
      self.arrival()
    if event.type == 'Partida':
      self.departure()

    if self.next_arrival < self.next_departure:
      if not self.events.isFull():
        self.arrival()
    else:
      if self.count_event_type('Chegada') > self.count_event_type('Partida'):
        self.departure()
  
  def run(self):
    sim.arrival()
    self.is_running = True
    while self.events and self.is_running and self.clock < self.max_time:
      if self.events.isEmpty():
        print('A fila de eventos está vazia')
        self.is_running = False
        break
      event = self.events.dequeue()
      self.process_event(event)
  
  def count_event_type(self, event_type):
    return len([event for event in self.events.queue if event.type == event_type and event.priority >= self.clock])

if __name__ == '__main__':
  max_size = 10
  max_time = 50
  arrival_rate = 0.5
  service_rate = 0.5

  sim = MM1Simulation(arrival_rate, service_rate, max_time, max_size)
  print(str(sim))
  # sim.generate_arrival()
  # print(str(sim))
  # event = sim.events.dequeue()
  # print(event)
  # sim.generate_arrival()
  # print(str(sim))
  sim.run()