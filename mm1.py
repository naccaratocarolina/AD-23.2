import numpy as np
from collections import deque
from public.common import *

class MM1:
  def __init__(self, arrival_rate, service_rate, max_iter, queue_len):
    self.arrival_rate = arrival_rate # Taxa de chegada
    self.service_rate = service_rate # Taxa de serviço
    self.max_iter = max_iter # Número máximo de iterações
    self.queue_len = queue_len # Tamanho da fila

    # Fila de clientes
    if self.queue_len == -1:
      self.queue = deque()
    elif self.queue_len > 0:
      self.queue = deque(maxlen=self.queue_len)
    else:
      raise ValueError("queue_len must be greater than 0 or equal to -1")

    self.wait_times = [] # Lista de tempos de espera dos clientes
    self.idle_times = [] # Lista de tempos ociosos do servidor
    self.is_idle = (False, 0) # Tupla que indica se o servidor está ocioso e o tempo em que ele ficou ocioso
    self.clock = 0 # Relógio de simulação
    self.next_arrival = self.generate_next_arrival()  # Próxima chegada
    self.next_departure = float('inf')  # Próxima partida (igual a infinito para forçar a chegada do primeiro cliente)

  def generate_next_arrival(self):
    # Modela fluxo de chegada poisson atraves do tempo entre chegadas com distribuição exponencial
    return np.random.exponential(1/self.arrival_rate)

  def generate_next_departure(self):
    # Gera o próximo tempo de partida com distribuição exponencial
    return np.random.exponential(1/self.service_rate)

  def arrival(self):
    # Processa a chegada de um cliente
    self.queue.append(self.clock)
    
    # Imprime log
    mm1_log(f'Cliente chega{RESET_COLOR} N = {len(self.queue)}', self.clock, 'arrival')
    
    # Se o servidor estiver ocioso, o cliente é atendido imediatamente
    if len(self.queue) == 1:
      self.next_departure = self.clock + self.generate_next_departure()
    
    # Gera a próxima chegada
    self.next_arrival = self.clock + self.generate_next_arrival()

  def departure(self):
    # Processa a partida de um cliente
    served = self.queue.popleft()
    
    # Calcula o tempo de espera do cliente
    wait_time = self.clock - served
    self.wait_times.append(wait_time)
    
    if self.is_idle[0]:
      # Calcula o tempo ocioso do servidor
      idle_time = self.clock - self.is_idle[1]
      self.idle_times.append(idle_time)
      self.is_idle = (False, 0)
      # Imprime tempo que o servidor ficou oscioso
      mm1_log(f'Servidor volta a atender clientes após {idle_time:.2f}{RESET_COLOR}', self.clock, 'idle')
    
    # Imprime log
    mm1_log(f'Cliente é atendido{RESET_COLOR} Tempo de espera: {wait_time:.2f}', self.clock, 'departure')

    # Se houver clientes na fila, agenda a partida do próximo cliente
    if len(self.queue) > 0:
      self.next_departure = self.clock + self.generate_next_departure()
    # Se não houver clientes na fila, o servidor fica ocioso
    else:
      self.is_idle = (True, self.clock)
      mm1_log(f'Servidor ocioso {RESET_COLOR}N = {len(self.queue)}', self.clock, 'idle')
      self.next_departure = float('inf') # Força com que o proximo evento seja uma chegada
  
  def handle_events(self):
    # Verifica qual evento ocorreu primeiro
    if self.next_arrival < self.next_departure:
      # Trata a chegada
      self.clock = self.next_arrival
      self.arrival()
    else:
      # Trata a partida
      self.clock = self.next_departure
      self.departure()

  def run_simulation(self, idle_server):
    has_max_iter = self.max_iter > 0
    
    # Gera primeira chegada
    self.arrival()

    # Loop de controle da simulação
    if has_max_iter and not idle_server:
      # Simula até o número máximo de iterações
      for _ in range(self.max_iter):
        self.handle_events()
    elif has_max_iter and idle_server:
      # Simula até o número máximo de iterações ou até o servidor ficar ocioso
      i = 0
      while i < self.max_iter and len(self.queue) > 0:
        self.handle_events()
        i += 1
    elif not has_max_iter and idle_server:
      # Simula até a fila ficar vazia
      while len(self.queue) > 0:
        self.handle_events()
    elif not has_max_iter and not idle_server:
      # Simula infinitamente
      while True:
        self.handle_events()

    print() # Pula uma linha
  
    return len(self.wait_times), self.clock

if __name__ == '__main__':
  # Parsear flags
  args = mm1_parse_flags()
  arrival_rate = args.arrival_rate
  service_rate = args.service_rate
  max_iter = args.max_iter
  queue_len = args.queue_len
  idle_server = args.idle_server
  num_sim = args.num_sim

  # Inicializar simulação
  for _ in range(num_sim):
    sim_log(f'Simulação {(_+1):02d}')
    mm1_sim = MM1(arrival_rate, service_rate, max_iter, queue_len)
    num_customers, final_time = mm1_sim.run_simulation(idle_server)

    # Imprimir estatísticas
    sim_log('Estatísticas:')
    print(f'Número de clientes atendidos: {num_customers}')
    print(f'Tempo médio de espera: {np.mean(mm1_sim.wait_times):.2f}')
    if len(mm1_sim.idle_times):
      print(f'Servidor ficou oscioso {len(mm1_sim.idle_times)} vezes com tempo médio de {np.mean(mm1_sim.idle_times):.2f}')
    print(f'Tempo final da simulação: {final_time:.2f}')
