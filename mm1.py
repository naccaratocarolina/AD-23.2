import math
import random
from collections import deque

class Event():
  def __init__(self, type, time):
    self._type = type
    self._time = time

  @property
  def type(self):
    return self._type

  @property
  def time(self):
    return self._time

  def __repr__(self):
    return '(%s, %f)' % (self.type, self.time)

class Queue():
  def __init__(self):
    self._queue = [] # Lista de eventos
    self._client = 0 # Numero de clientes
  
  @property
  def queue(self):
    return self._queue

  @property
  def client(self):
    return self._client
  
  def enqueue(self, event):
    self._client += 1
    # Inserir evento na lista de eventos
    self._queue.append(event)
    # Ordenar lista de eventos
    self._queue.sort(key=lambda x: x.time)
    # Retornar numero do cliente
    return self._client
  
  def dequeue(self):
    # Retirar primeiro evento da lista de eventos
    self._queue.pop(0)
    # Retornar numero do cliente atendido
    return self._client
  
  def is_empty(self):
    # Verificar se lista de eventos está vazia
    return len(self._queue) == 0

  def __repr__(self):
    return str(self._queue)

class MM1():
  def __init__(self, server_rate, arrival_rate, DEBUG = False):
    self.DEBUG = DEBUG # Inicializar variável de debug
    self.N = 0 # Inicializar variavel de estado
    self.L = [] # Inicializar lista de eventos
    self.queue = Queue() # Cliente no servidor
    self.server_rate = server_rate # Taxa de serviço do servidor
    self.arrival_rate = arrival_rate # Taxa de chegada de clientes
    self.clock = 0 # Inicializar relógio do simulador (eventos/time unit)
    self.next_arrival = self.generate_arrival() # Sortear tempo da próxima chegada
    self.next_departure = math.inf # Inicializar tempo da próxima partida com infinito
  
  def generate_arrival(self):
    # Sortear tempo da próxima chegada de acordo com distribuição exponencial
    return random.expovariate(self.arrival_rate)
  
  def generate_departure(self):
    # Sortear tempo de partida de acordo com distribuição exponencial
    return random.expovariate(self.server_rate)
  
  # Handler para evento de chegada
  def arrival(self):
    # Incrementar número de clientes na fila
    self.N += 1

    # Sortear tempo da próxima chegada
    self.next_arrival = self.generate_arrival()

    # Atualizar relógio do simulador
    self.clock += self.next_arrival

    # Novo evento de chegada
    arrival_event = Event('arrival', self.clock)

    # Incluir evento na lista L
    self.L.append(arrival_event)

    # Incluir cliente na fila
    arrived = self.queue.enqueue(arrival_event)

    if self.DEBUG:
      print('Cliente #%d chegou no instante %f' % (arrived, self.clock))

    # Se N = 1, cliente passa a ser atendido imediatamente
    if self.N == 1:
      # Sortear tempo de partida
      self.next_departure = self.generate_departure()

      # Atualizar relógio do simulador
      self.clock += self.next_departure

      # Incluir evento na lista L
      self.L.append(Event('departure', self.clock))

      # Retirar cliente da fila
      served = self.queue.dequeue()

      if self.DEBUG:
        print('Cliente #%d atendido no instante %f' % (served, self.clock))

  # Handler para evento de partida
  def departure(self):
    # Decrementar número de clientes na fila
    self.N -= 1

    # Se N > 0, cliente no início da fila passa a ser atendido
    if self.N > 0:
      # Sortear tempo de partida
      self.next_departure = self.generate_departure()

      # Atualizar relógio do simulador
      self.clock += self.next_departure

      # Incluir evento na lista L
      self.L.append(Event('departure', self.clock))

      # Retirar cliente da fila
      served = self.queue.dequeue()

      if self.DEBUG:
        print('Cliente #%d atendido no instante %f' % (served, self.clock))

class Simulator():
  def __init__(self, arrival_rate, server_rate, max_events, DEBUG=False):
    self.DEBUG = DEBUG
    self.arrival_rate = arrival_rate
    self.server_rate = server_rate
    self.max_events = max_events
  
  def run(self):
    simulator = MM1(self.server_rate, self.arrival_rate, self.DEBUG)

    # Evento inicial: Chegada de cliente
    simulator.arrival()

    # Quantidade de eventos processados
    processed_events = 0

    # Loop principal do simulador
    while simulator.L and processed_events < self.max_events:
      # Retirar primeiro evento da lista e tratar evento
      e = simulator.L.pop(0)
      processed_events += 1

      if simulator.DEBUG:
        print('Evento do tipo %s no instante %f' % (e.type, e.time))

      # Se evento for do tipo chegada, tratar chegada
      if e.type == 'arrival':
        simulator.arrival()
      # Se evento for do tipo partida, tratar partida
      elif e.type == 'departure':
        simulator.departure()
    
    return simulator.clock

  def little_law(self, arrival_rate, server_rate):
    return arrival_rate/(server_rate - arrival_rate)

# Plano de controle: Loop principal do simulador
if __name__ == '__main__':
  server_rate = 0.6  # Taxa de serviço do servidor
  arrival_rate = 0.3 # Taxa de chegada de clientes
  max_events = 10 # Número máximo de eventos a serem processados

  # Inicializar simulador
  simulator = Simulator(arrival_rate, server_rate, max_events, True)

  # Executar simulador
  clock = simulator.run()

  # Imprimir tempo de simulação
  print('Tempo de simulação: %f' % clock)