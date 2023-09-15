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

class MM1():
  def __init__(self, server_rate, arrival_rate, DEBUG = False):
    self.DEBUG = DEBUG # Inicializar variável de debug
    self.N = 0 # Inicializar variavel de estado
    self.L = [] # Inicializar lista de eventos
    self.server_rate = server_rate # Taxa de serviço do servidor
    self.arrival_rate = arrival_rate # Taxa de chegada de clientes
    self.clock = 0 # Inicializar relógio do simulador
    self.next_arrival = self.generate_arrival() # Sortear tempo da próxima chegada
    self.next_departure = math.inf # Inicializar tempo da próxima partida com infinito
  
  def generate_arrival(self):
    # Sortear tempo da próxima chegada de acordo com distribuição exponencial
    return -1/self.arrival_rate * math.log(random.random())
  
  def generate_departure(self):
    # Sortear tempo de partida de acordo com distribuição exponencial
    return -1/self.server_rate * math.log(random.random())
  
  # Handler para evento de chegada
  def arrival(self):
    # Incrementar número de clientes na fila
    self.N += 1

    # Sortear tempo da próxima chegada
    self.next_arrival = self.generate_arrival()

    # Atualizar relógio do simulador
    self.clock += self.next_arrival

    # Incluir evento na lista L
    self.L.append(Event('arrival', self.clock))

    # Se N = 1, cliente passa a ser atendido imediatamente
    if self.N == 1:
      # Sortear tempo de partida
      self.next_departure = self.generate_departure()

      # Atualizar relógio do simulador
      self.clock += self.next_departure

      # Incluir evento na lista L
      self.L.append(Event('departure', self.clock))

    if self.DEBUG:
      print('Chegada do cliente #%d no instante %f' % (self.N, self.clock))
    
  # Handler para evento de partida
  def departure(self):
    if self.DEBUG:
      print('Partida do cliente #%d no instante %f' % (self.N, self.clock))

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


# Plano de controle: Loop principal do simulador
if __name__ == '__main__':
  server_rate = 0.5 # Taxa de serviço do servidor
  arrival_rate = 0.5 # Taxa de chegada de clientes

  simulator = MM1(server_rate, arrival_rate, True) # Inicializar simulador

  # Evento inicial: Chegada de cliente
  simulator.arrival()

  # Número máximo de eventos processados
  max_events = 10

  # Quantidade de eventos processados
  processed_events = 0

  # Loop principal do simulador
  # Enquanto L não estiver vazia, faça:
  while len(simulator.L) > 0 and processed_events < max_events:
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
  
  if simulator.DEBUG:
    print('Tempo de simulação: ', simulator.clock)