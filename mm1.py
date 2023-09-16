from queue import Queue
import random
import math

class Event():
  def __init__(self, id, type, time):
    self._id = id # Identificador do evento
    self._type = type # Chegada (arrival) ou partida (departure)
    self._time = time # Tempo de ocorrência do evento
  
  @property
  def id(self):
    return self._id

  @property
  def type(self):
    return self._type
  
  @property
  def time(self):
    return self._time

class mm1():
  def __init__(self, server_rate, arrival_rate, max_size = 100):
    self.server_rate = server_rate # Taxa de serviço do servidor
    self.arrival_rate = arrival_rate # Taxa de chegada de clientes
    self.max_size = max_size # Número máximo de chegadas
    self.N = 0 # Número de clientes na fila
    self.total_arrivals = 0
    self.L = Queue(max_size) # Lista de eventos
    self.clock = 0 # Relógio do simulador (eventos/time unit)
    self.next_arrival = self.generate_arrival() # Sortear tempo da próxima chegada
    self.next_departure = math.inf # Inicializar tempo da próxima partida com infinito
  
  def print_queue(self):
    if self.L.empty():
      print('[]')
    else:
      for event in self.L.queue:
        print(f'#{event.id}', end = ' ')
    print()
  
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
    self.total_arrivals += 1
    event = Event(self.total_arrivals, 'arrival', self.clock)

    # Incluir evento na lista L
    if not self.L.full():
      self.L.put(event)
    else:
      print('Fila cheia!')

    # Printa log de chegada
    print('Cliente #%d chegou no instante %f' % (event.id, self.clock))

    # Imprime fila
    self.print_queue()

    # Se N = 1, cliente passa a ser atendido imediatamente
    #if self.N == 1:
      #self.departure(True)
  
  def departure(self, force = False):
    # Decrementar número de clientes na fila
    self.N -= 1

    if self.N > 0 or force:
      # Sortear tempo de partida
      self.next_departure = self.generate_departure()

      # Atualizar relógio do simulador
      self.clock += self.next_departure

      # Retira cliente da fila
      event = self.L.get()

      # Novo evento de partida
      event = Event(event.id, 'departure', self.clock)

      # Printa log de partida
      print('Cliente #%d atendido no instante %f' % (event.id, self.clock))
    else:
      print('Servidor ocioso no instante %f' % (self.clock))
  
# Plano de controle: Loop principal do simulador
if __name__ == '__main__':
  server_rate = 1.0 # Taxa de serviço do servidor
  arrival_rate = 0.5 # Taxa de chegada de clientes
  max_arrivals = 10 # Número máximo de chegadas

  # Inicializar simulador
  simulator = mm1(server_rate, arrival_rate, max_arrivals)

  # Evento inicial de chegada
  simulator.arrival()

  # Quantidade de eventos atendidos
  processed_events = 0

  while simulator.L.qsize() > 0 and processed_events < max_arrivals:
    # Incrementar quantidade de eventos atendidos
    processed_events += 1

    # Obter próximo evento
    event = simulator.L.get()

    # Chegada
    if event.type == 'arrival':
      simulator.arrival()
    # Partida
    elif event.type == 'departure':
      simulator.departure()