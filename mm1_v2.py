import numpy as np

# Cores para print
SIM_COLOR = '\033[30m' # Preto
SIM_BACKGROUND_COLOR = '\033[47m' # Fundo branco
ARRIVAL_COLOR = '\033[33m' # Amarelo
DEPARTURE_COLOR = '\033[34m' # Azul
RESET_COLOR = '\033[0m'

class MM1:
  def __init__(self, arrival_rate, service_rate, max_iter):
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
    self.max_iter = max_iter

    self.queue = []  # Fila de clientes
    self.wait_times = []  # Lista de tempos de espera dos clientes
    self.clock = 0 # Relógio de simulação
    self.next_arrival = self.generate_next_arrival()  # Próxima chegada
    self.next_departure = float('inf')  # Próxima partida

  def generate_next_arrival(self):
    # Gera o próximo tempo de chegada com distribuição Poisson
    return np.random.poisson(self.arrival_rate)

  def generate_next_departure(self):
    # Gera o próximo tempo de partida com distribuição exponencial
    return np.random.exponential(1/self.service_rate)

  def arrival(self):
    # Processa a chegada de um cliente
    print(f'{ARRIVAL_COLOR}{self.clock:.2f}: Cliente chega{RESET_COLOR}')
    self.queue.append(self.clock)
      
    if len(self.queue) == 1:
      self.next_departure = self.clock + self.generate_next_departure()
      
    self.next_arrival = self.clock + self.generate_next_arrival()

  def departure(self):
    # Processa a partida de um cliente
    served = self.queue.pop(0)
    wait_time = self.clock - served
    self.wait_times.append(wait_time)
    print(f'{DEPARTURE_COLOR}{self.clock:.2f}: Cliente é atendido{RESET_COLOR} Tempo de espera: {wait_time:.2f}')

    if len(self.queue) > 0:
      self.next_departure = self.clock + self.generate_next_departure()
    else:
      print(f'{self.clock:.2f} Servidor oscioso')
      self.next_departure = float('inf') # Força com que o proximo evento seja uma chegada

  def run_simulation(self):
    # Gera primeira chegada
    self.arrival()

    for _ in range(self.max_iter):
      if self.next_arrival < self.next_departure:
        self.clock = self.next_arrival
        self.arrival()
      else:
        self.clock = self.next_departure
        self.departure()
  
    return len(self.wait_times), self.clock

if __name__ == '__main__':
  arrival_rate = 2  # Taxa de chegada de clientes
  service_rate = 1  # Taxa de serviço do servidor
  max_iter = 10   # Número máximo de iterações

  mm1_sim = MM1(arrival_rate, service_rate, max_iter)
  num_customers, final_time = mm1_sim.run_simulation()

  print('\nEstatísticas:')
  print(f'Número de clientes atendidos: {num_customers}')
  print(f'Tempo final da simulação: {final_time:.2f}')
