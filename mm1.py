import random
import simpy
import math
from collections import deque

class mm1():
  def __init__(self, env, num_servers, arrival_rate, service_rate):
    self.env = env # Ambiente de simulação
    self.server = simpy.Resource(env, num_servers) # Servidor
    self.arrival_rate = arrival_rate # Taxa de chegada
    self.service_rate = service_rate # Taxa de serviço
    self.queue = deque() # Fila de clientes
    self.in_system = [(0,0)] # Tempo atual da simulação e número de clientes no sistema
    self.wait_times = [] # Lista de tempos de espera dos clientes
    self.next_arrival = self.generate_next_arrival() # Gerador de chegadas
    self.next_departure = math.inf # Tempo da próxima partida

  def generate_next_arrival(self):
    # Sortear tempo da próxima chegada de acordo com distribuição exponencial
    return random.expovariate(self.arrival_rate)

  def generate_next_departure(self):
    # Sortear tempo de partida de acordo com distribuição exponencial
    return random.expovariate(self.service_rate)

  def generate_arrival(self):
    # Gera chegada de cliente baseado na proxima chegada
    yield self.env.timeout(self.next_arrival)
  
  def generate_departure(self):
    # Gera partida de cliente baseado na proxima partida
    yield self.env.timeout(self.next_departure)
  
  # Handler para evento de chegada
  def arrival(self):
    print('%g: Cliente chega (num_in_system=%d->%d)' % 
      (self.env.now, len(self.queue), len(self.queue)+1))

    # Adiciona evento no final da fila
    self.queue.append(self.env.now)
    self.in_system.append((self.env.now, len(self.queue)))

    # Agenda chegada do próximo cliente
    with self.server.request() as request:
      yield request
      yield self.env.process(self.generate_arrival())
    
    # Se houver somente 1 cliente no sistema, ele passa a ser atendido imediatamente
    if len(self.queue) == 1:
      # Agenda partida do próximo cliente
      with self.server.request() as request:
        yield request
        yield self.env.process(self.generate_departure())

  # Handler para evento de partida
  def departure(self):
    print('%g: Cliente sai (num_in_system=%d->%d)' % 
      (self.env.now, len(self.queue), len(self.queue)-1))

    # Remove cliente do início da fila
    served = self.queue.popleft()
    self.in_system.append((self.env.now, len(self.queue)))
    self.wait_times.append(self.env.now - served)

    # Se houver clientes na fila, o próximo cliente passa a ser atendido
    if len(self.queue) > 0:
      # Agenda partida do próximo cliente
      with self.server.request() as request:
        yield request
        yield self.env.process(self.generate_departure())
  
def run(env, num_servers, arrival_rate, service_rate):
  # Inicializar simulador
  mm1_sim = mm1(env, num_servers, arrival_rate, service_rate)

  # Agendar primeira chegada
  env.process(mm1_sim.arrival())

  # Executar simulação
  while True:
    # Aguardar próximo evento de chegada
    yield env.timeout(mm1_sim.next_arrival)
    env.process(mm1_sim.arrival())

if __name__ == '__main__':
  server_rate = 1.0 # Taxa de serviço do servidor
  arrival_rate = 0.5 # Taxa de chegada de clientes

  # Inicializar simulador
  env = simpy.Environment()
  env.process(run(env, 1, arrival_rate, server_rate))
  env.run(until=5)