class Event():
  def __init__(self, type, priority):
    self.type = type # Tipo do evento
    self.priority = priority # Prioridade do evento
  
  def __str__(self):
    return f'{self.type} ({self.priority:.2f})'

class PriorityQueue():
  def __init__(self, max_size, sort=min):
    self.queue = [] # Lista de eventos
    self.max_size = self.parse_max_size(max_size) # Tamanho máximo da lista
    self.sort = sort # Se é min ou max heap
  
  @property
  def size(self):
    return len(self.queue)
  
  @staticmethod
  def parse_max_size(size):
    if size < 0: # Valor negativo significa infinito
      return float('inf')
    elif size == 0: # Valor 0 não faz sentido
      raise Exception('A fila não pode ter tamanho 0')
    else: # Valor positivo
      return int(size)
  
  def isEmpty(self):
    return self.size == 0
  
  def isFull(self):
    return self.size == self.max_size
  
  def enqueue(self, event):
    if self.isFull():
      print(f'A fila está cheia. Evento {event} desprezado')
      return
    self.queue.append(event)
    self.queue = sorted(self.queue, key=lambda event: event.priority)
  
  def dequeue(self):
    if self.isEmpty():
      print('A fila está vazia')
      return
    return self.queue.pop(0)  
  
  def __str__(self):
    if self.isEmpty():
      return '[]'
    return f'[{", ".join([str(event) for event in self.queue])}]'

class Simulation():
  def __init__(self, max_time, max_size, sort=min):
    self.clock = 0 # Tempo atual
    self.events = PriorityQueue(max_size, sort) # Fila de eventos
    self.max_time = self.parse_max_time(max_time) # Tempo máximo de simulação
    self.is_running = False # Se o servidor está ocupado ou ocioso
  
  @staticmethod
  def parse_max_time(time):
    if time < 0:
      return float('inf')
    elif time == 0:
      raise Exception('O tempo máximo de simulação não pode ser 0')
    else:
      return time
  
  def schedule_event(self, event):
    if not event == None:
      self.events.enqueue(event)
  
  def process_event(self, event):
    print(f'{self.clock:.2f}: Processando evento {event}')

  def run(self):
    self.is_running = True
    while self.events and self.is_running and self.clock < self.max_time:
      if self.events.isEmpty():
        print('A fila de eventos está vazia')
        break
      event = self.events.dequeue()
      self.clock += event.priority
      self.process_event(event)
  
  def stop(self):
    self.is_running = False
  
  def reset(self):
    self.clock = 0
    self.events = PriorityQueue(self.events.max_size, self.events.sort)
    self.is_running = False
  
  def __str__(self):
    return f'{self.clock:.2f} Fila: {self.events}'

if __name__ == '__main__':
  sim = Simulation(20, 4)
  sim.schedule_event(Event('Tipo 1', 10))
  sim.schedule_event(Event('Tipo 2', 5))
  sim.schedule_event(Event('Tipo 3', 1))
  sim.schedule_event(Event('Tipo 2', 9))
  sim.schedule_event(Event('Tipo 1', 3))
  sim.schedule_event(Event('Tipo 3', 2))
  sim.schedule_event(Event('Tipo 2', 4))
  sim.schedule_event(Event('Tipo 1', 7))
  sim.schedule_event(Event('Tipo 1', 6))
  print(str(sim))
  sim.run()