import numpy as np

DEPARTURE_COLOR = '\033[94m' # Azul
END_COLOR = '\033[0m' # Branco

class Event:
  def __init__(self, type, priority):
    self.type = type
    self.priority = priority
  
  def __str__(self):
    return f'{self.type} ({self.priority:.2f})'

class Arrival(Event):
  def __init__(self, arrival_rate):
    self.arrival_rate = arrival_rate
    self.next_arrival = self.generate_next_arrival(arrival_rate)
    self.color = '\033[93m' # Amarelo
    super().__init__('Arrival', self.next_arrival)

  def generate_next_arrival(self, arrival_rate):
    return np.random.exponential(1 / arrival_rate)
  
  def __str__(self):
    return f'{self.color}{self.type} Tempo entre chegadas: {self.priority:.2f}{END_COLOR}'

class Departure(Event):
  def __init__(self, service_rate):
    self.service_rate = service_rate
    self.next_departure = self.generate_next_departure(service_rate)
    self.color = '\033[94m' # Azul
    super().__init__('Departure', self.next_departure)

  def generate_next_departure(self, service_rate):
    return np.random.exponential(1 / service_rate)
  
  def __str__(self):
    return f'{self.color}{self.type} Tempo de serviço: {self.priority:.2f}{END_COLOR}'

class PriorityQueue():
  def __init__(self, max_size):
    self.queue = []
    self.max_size = max_size
  
  def __str__(self):
    if self.isEmpty():
      return '[]'
    return f'[{", ".join([x.type for x in self.queue])}]'

  def isEmpty(self):
    return len(self.queue) == 0
  
  def isFull(self):
    return len(self.queue) == self.max_size
  
  def size(self):
    return len(self.queue)
  
  # Adiciona evento na fila se ela não estiver cheia
  def add(self, event):
    if not isinstance(event, Event):
      raise ValueError('Cada elemento da fila deve ser um evento')

    if self.isFull():
      return False
    else:
      self.queue.append(event)
      return True
  
  # Remove evento com maior prioridade
  def pop(self):
    if not self.isEmpty():
      highest = min(self.queue, key=lambda x: x.priority)
      self.queue.remove(highest)
      return highest
    else:
      return -1

class Simulation():
  def __init__(self, max_size=100):
    self.clock = 0 # Tempo atual
    self.events = PriorityQueue(max_size)
    self.is_running = False
  
  def process_event(self, event):
    raise NotImplementedError('Método não implementado')

  def schedule_event(self, event):
    self.events.add(event)
  
  def run(self):
    self.is_running = True
    while self.events and self.is_running:
      event = self.events.pop()
      self.clock += event.priority
      self.process_event(event)
  
  def stop(self):
    self.is_running = False
  
  def reset(self):
    self.clock = 0
    self.events = PriorityQueue(self.events.max_size)
    self.is_running = False

class MM1Simulation(Simulation):
  def __init__(self, arrival_rate, service_rate, max_size, simulation_time):
    super().__init__(max_size)
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
    self.max_size = max_size
    self.simulation_time = simulation_time
  
  def generate_arrival(self):
    return Arrival(self.arrival_rate)

  def generate_departure(self):
    return Departure(self.service_rate)
  
  def process_event(self, event):
    if event.type == 'Arrival':
      # Gera próximo evento de chegada
      next_arrival = self.generate_arrival()

      # Agenda evento de chegada
      self.schedule_event(next_arrival)

      # Se servidor estiver livre, gera evento de saída
      if self.events.isEmpty():
        next_departure = self.generate_departure()
        self.schedule_event(next_departure)
      else:
        # Se servidor estiver ocupado, verifica se há espaço na fila
        if not self.events.isFull():
          # Se houver espaço na fila, adiciona evento de saída
          next_departure = self.generate_departure()
          self.schedule_event(next_departure)
        else:
          # Se não houver espaço na fila, cliente vai embora
          print(f'{self.clock:.2f}: Cliente desprezado')
          pass
    elif event.type == 'Departure':
      # Gera próximo evento de saída
      next_departure = self.generate_departure()

      # Agenda evento de saída
      self.schedule_event(next_departure)
  
  def run(self):
    self.is_running = True

    # Simulação começa com a chegada do primeiro cliente
    first_arrival = self.generate_arrival()
    self.schedule_event(first_arrival)

    condition = self.clock < self.simulation_time and self.is_running

    while condition:
      event = self.events.pop()
      self.clock += event.priority

      if self.clock >= self.simulation_time:
        self.stop()
        break
      
      self.process_event(event)
      # print(self.events)
      print(f'{self.clock:.2f}: {event}')

    self.is_running = False

if __name__ == '__main__':
  max_size = 4
  max_time = 20
  arrival_rate = 0.5
  service_rate = 0.5
  
  mm1 = MM1Simulation(arrival_rate, service_rate, max_size, max_time)
  mm1.run()
  


