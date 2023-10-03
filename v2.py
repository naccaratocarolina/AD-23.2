import numpy as np
from utils import *

ARRIVAL_COLOR = '\033[93m' # Amarelo
DEPARTURE_COLOR = '\033[94m' # Azul
END_COLOR = '\033[0m' # Branco

# Eventos da simulação de fila M/M/1
class Arrival(Event):
  def __init__(self, arrival_rate, clock):
    self.arrival_rate = arrival_rate
    self.next_arrival = self.generate_next_arrival(arrival_rate)
    self.priority = clock + self.next_arrival
    super().__init__('Chegada', self.priority)
  
  def generate_next_arrival(self, arrival_rate):
    return np.random.exponential(1 / arrival_rate)
  
  def next(self):
    return self.next_arrival

class Departure(Event):
  def __init__(self, service_rate, clock):
    self.service_rate = service_rate
    self.next_departure = self.generate_next_departure(service_rate)
    self.priority = clock + self.next_departure
    super().__init__('Partida', self.priority)
  
  def generate_next_departure(self, service_rate):
    return np.random.exponential(1 / service_rate)
  
  def next(self):
    return self.next_departure

# Simulação de fila M/M/1
class MM1Simulation(Simulation):
  def __init__(self, arrival_rate, service_rate, max_time, max_size):
    self.sort = min
    super().__init__(max_time, max_size, self.sort)
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
  
  def generate_arrival(self):
    # A geraçao de uma chegada implicará na geração de uma partida
    next_arrival = Arrival(self.arrival_rate, self.clock)
    self.schedule_event(next_arrival)
    next_departure = self.generate_departure()
    if next_departure:
      next_departure.priority += next_arrival.priority
      self.schedule_event(next_departure)
  
  def generate_departure(self):
    # Não permite geração de evento de partida se não houver evento de chegada correspondente
    arrivals = self.count_event_type('Chegada')
    departures = self.count_event_type('Partida')
    if departures < arrivals:
      return Departure(self.service_rate, self.clock)
  
  def process_event(self, event):
    if event.type == 'Chegada':
      print(f'{ARRIVAL_COLOR}{self.clock:.2f}: Processando evento {event}{END_COLOR}')
      self.generate_arrival()
    elif event.type == 'Partida':
      print(f'{DEPARTURE_COLOR}{self.clock:.2f}: Processando evento {event}{END_COLOR}')
      next_departure = self.generate_departure()
      if next_departure:
        next_departure.priority += self.clock
        self.schedule_event(next_departure)
    else:
      raise Exception('Tipo de evento inválido')
  
  def run(self):
    self.is_running = True
    while self.events and self.is_running and self.clock < self.max_time:
      if self.events.isEmpty():
        print('A fila de eventos está vazia')
        break
      event = self.events.dequeue()
      self.clock += event.next()
      self.process_event(event)
      print(str(self))
  
  def count_event_type(self, event_type):
    return len([event for event in self.events.queue if event.type == event_type])

if __name__ == '__main__':
  max_size = 10
  max_time = 100
  arrival_rate = 0.5
  service_rate = 0.5

  sim = MM1Simulation(arrival_rate, service_rate, max_time, max_size)
  sim.generate_event()
  # sim.generate_arrival()
  # print(str(sim))
  # event = sim.events.dequeue()
  # print(event)
  # sim.generate_arrival()
  # print(str(sim))
  sim.run()