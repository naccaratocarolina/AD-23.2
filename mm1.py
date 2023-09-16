import random
import simpy
import math
from collections import deque

# Cores para print
SIM_COLOR = '\033[30m' # Preto
SIM_BACKGROUND_COLOR = '\033[47m' # Fundo branco
ARRIVAL_COLOR = '\033[33m' # Amarelo
DEPARTURE_COLOR = '\033[34m' # Azul
RESET_COLOR = '\033[0m'

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
    self.mm1_log(True)

    # Adiciona evento no final da fila
    self.queue.append(self.env.now)
    self.in_system.append((self.env.now, len(self.queue)))

    # Sortear tempo da próxima chegada
    self.next_arrival = self.generate_next_arrival()

    # Agenda chegada do próximo cliente
    with self.server.request() as request:
      yield request
      yield self.env.process(self.generate_arrival())
    
    # Atualizar tempo da próxima partida
    if (self.next_departure == math.inf):
      self.env.process(self.departure())
    
    # Se houver somente 1 cliente no sistema, ele passa a ser atendido imediatamente
    if len(self.queue) == 1:
      # Agenda partida do próximo cliente
      with self.server.request() as request:
        yield request
        yield self.env.process(self.generate_departure())

  # Handler para evento de partida
  def departure(self):
    # Se houver clientes na fila, o próximo cliente passa a ser atendido
    if len(self.queue) > 0:
      self.mm1_log(False)

      # Remove cliente do início da fila
      served = self.queue.popleft()
      self.in_system.append((self.env.now, len(self.queue)))
      self.wait_times.append(self.env.now - served)

      # Sortear tempo da próxima partida
      self.next_departure = self.generate_next_departure()
      # Agenda partida do próximo cliente
      with self.server.request() as request:
        yield request
        yield self.env.process(self.generate_departure())
  
  def mm1_log(self, event_type):
    size = len(self.queue)
    if event_type:
      print(f"{ARRIVAL_COLOR}{self.env.now:.2f}: Cliente chega (num_in_system={size}->{size-1}){RESET_COLOR}") 
    else:
      print(f"{DEPARTURE_COLOR}{self.env.now:.2f}: Cliente sai (num_in_system={size}->{size-1}){RESET_COLOR}")

def run(mm1_sim):
  # Agendar primeira chegada
  env.process(mm1_sim.arrival())

  # Executar simulação
  while True:
    # Aguarda proximo evento de chegada ou partida
    yield env.any_of([env.timeout(mm1_sim.next_arrival), env.timeout(mm1_sim.next_departure)])

    if mm1_sim.next_arrival < mm1_sim.next_departure:
      # Chegada
      env.process(mm1_sim.arrival())
    else:
      # Partida
      env.process(mm1_sim.departure())

def sim_log(env, msg):
  print(f"{SIM_COLOR}{SIM_BACKGROUND_COLOR}{env.now:.2f}: {msg}{RESET_COLOR}")

if __name__ == '__main__':
  server_rate = 0.5 # Taxa de serviço do servidor
  arrival_rate = 0.5 # Taxa de chegada de clientes

  # Inicializar simulador
  env = simpy.Environment()
  # random.seed(42) # Adicionando semente para geração de números aleatórios
  sim_log(env, 'Inicializando simulador')
  mm1_sim = mm1(env, 1, arrival_rate, server_rate)
  env.process(run(mm1_sim))
  env.run(until=10)
  sim_log(env, 'Simulação finalizada')
  