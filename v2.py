import numpy as np
from utils import *

ARRIVAL_COLOR = '\033[93m' # Amarelo
DEPARTURE_COLOR = '\033[94m' # Azul
END_COLOR = '\033[0m' # Branco

# Eventos da simulação de fila M/M/1
class Arrival(Event):
  def __init__(self, arrival_rate):
    self.arrival_rate = arrival_rate
    self.next_arrival = self.generate_next_arrival(arrival_rate)
    super().__init__('Chegada', self.next_arrival)
  
  def generate_next_arrival(self, arrival_rate):
    return np.random.exponential(1 / arrival_rate)

class Departure(Event):
  def __init__(self, service_rate):
    self.service_rate = service_rate
    self.next_departure = self.generate_next_departure(service_rate)
    super().__init__('Partida', self.next_departure)
  
  def generate_next_departure(self, service_rate):
    return np.random.exponential(1 / service_rate)

# Simulação de fila M/M/1
class MM1Simulation(Simulation):
  def __init__(self, arrival_rate, service_rate, max_time, max_size):
    super().__init__(max_time, max_size, min)
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
    self.next_arrival = 0
    self.next_departure = float('inf')
  
  def generate_arrival(self):
    return Arrival(self.arrival_rate)
  
  def generate_departure(self):
    # Não permite geração de evento de partida se não houver evento de chegada correspondente
    arrivals = self.count_event_type('Chegada')
    departures = self.count_event_type('Partida')
    if departures < arrivals:
      return Departure(self.service_rate)
  
  def count_event_type(self, event_type):
    return len([event for event in self.events.queue if event.type == event_type])

if __name__ == '__main__':
  max_size = 4
  max_time = 10
  arrival_rate = 0.5
  service_rate = 0.5

  sim = MM1Simulation(arrival_rate, service_rate, max_time, max_size)
  sim.schedule_event(sim.generate_arrival())
  sim.schedule_event(sim.generate_arrival())
  sim.schedule_event(sim.generate_departure())
  sim.schedule_event(sim.generate_departure())
  sim.schedule_event(sim.generate_departure())
  print(str(sim))
  sim.run()