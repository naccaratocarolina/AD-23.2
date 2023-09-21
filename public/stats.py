import matplotlib.pyplot as plt
import numpy as np

class Stats():
  def __init__(self, mm1):
    self.mm1 = mm1
  
  def confidence_interval(self, data):
    n = len(data)
    mean = sum(data) / n
    std = np.std(data)
    h = std * 1.96 / np.sqrt(n)
    return [mean - h, mean + h]

  # Número médio simulado de pessoas na fila
  def avg_queue_len_sim(self):
    avg_len_sim = []
    total_queue_len = 0
    num_iter = len(self.mm1.wait_times)

    # Nenhum cliente foi atendido, logo o tamanho médio da fila é 0
    if num_iter == 0:
      return avg_len_sim
    
    # Calcula o tamanho médio da fila
    for i in range(num_iter):
      _, wait_time = self.mm1.wait_times[i]
      _, prev_wait_time = self.mm1.wait_times[i - 1] if i > 0 else (0, 0)
      _, idle_time = self.mm1.idle_times[i] if i < len(self.mm1.idle_times) else (0, 0)
      _, prev_idle_time = self.mm1.idle_times[i - 1] if i < len(self.mm1.idle_times) and i > 0 else (0, 0)

      if i == 0:
        queue_len = 1 # Primeiro cliente sendo servido
      else:
        queue_len += 1 if wait_time > prev_wait_time else 0
        queue_len -= 1 if i < len(self.mm1.idle_times) and idle_time > prev_idle_time else 0
      
      total_queue_len += queue_len
      avg_len_sim.append(total_queue_len / (i + 1))
    
    return avg_len_sim

  def plot_avg_queue_len(self):
    # Calcular tamanho médio da fila simulado
    avg_len_values = self.avg_queue_len_sim()
    num_iter = len(avg_len_values)

    if num_iter == 0:
      return

    # Calcula intervalo de confiança
    ci = self.confidence_interval(avg_len_values)
    upper_ci = [avg + (ci[1] - ci[0]) / 2 for avg in avg_len_values]
    lower_ci = [avg - (ci[1] - ci[0]) / 2 for avg in avg_len_values]

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(range(num_iter), avg_len_values, color='blue', label='Simulado')
    plt.plot(range(num_iter), upper_ci, color='red', alpha=0.5, linestyle='dashed', label='Intervalo de confiança superior')
    plt.plot(range(num_iter), lower_ci, color='red', alpha=0.5, linestyle='dashed', label='Intervalo de confiança inferior')
    plt.xlabel('Iteração')
    plt.ylabel('Número médio de pessoas na fila')
    plt.title('Número médio de pessoas na fila x Iteração')
    plt.legend()
    plt.grid(True)
    plt.show()

  # Gráfico do tempo médio na fila de espera
  def avg_wait_time(self):
    times = []
    avg_wait = []
    total_wait = 0

    for i, (clock, wait_time) in enumerate(self.mm1.wait_times, start=1):
      total_wait += wait_time
      times.append(clock)
      avg_wait.append(total_wait / (i + 1))
    
    return (times, avg_wait)

  def plot_avg_wait_time(self):
    times, avg_wait_values = self.avg_wait_time()
    num_iter = len(avg_wait_values)

    if num_iter == 0:
      return
    
    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(times, avg_wait_values, color='brown', label='Simulado', marker='o')
    plt.xlabel('Iteração')
    plt.ylabel('Tempo médio de espera')
    plt.title('Tempo médio de espera x Iteração')
    plt.legend()
    plt.grid(True)
    plt.show()

  # Gráfico do tempo médio de serviço
  def avg_service_time(self):
    avg_service = []
    times = []
    total_service = 0

    for i, (clock, service_time) in enumerate(self.mm1.service_times, start=1):
      total_service += service_time
      times.append(clock)
      avg_service.append(total_service / (i + 1))
    
    return times, avg_service

  def plot_avg_service_time(self):
    times, avg_service_values = self.avg_service_time()
    num_iter = len(avg_service_values)

    if num_iter == 0:
      return
    
    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(times, avg_service_values, color='blue', label='Simulado', marker='o')
    plt.xlabel('Iteração')
    plt.ylabel('Tempo médio de serviço')
    plt.title('Tempo médio de serviço x Iteração')
    plt.legend()
    plt.grid(True)
    plt.show()

  # Gráfico do tempo médio ocioso do servidor
  def avg_idle_server(self):
    avg_idle = []
    times = []
    total_idle = 0

    for i, (clock, idle_time) in enumerate(self.mm1.idle_times, start=1):
      total_idle += idle_time
      times.append(clock)
      avg_idle.append(total_idle / (i + 1))
    
    return times, avg_idle

  def plot_avg_idle_server(self):
    times, avg_idle_values = self.avg_idle_server()
    num_iter = len(avg_idle_values)

    if num_iter == 0:
      return
    
    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(times, avg_idle_values, color='magenta', label='Simulado', marker='o')
    plt.xlabel('Iteração')
    plt.ylabel('Tempo médio ocioso do servidor')
    plt.title('Tempo médio ocioso do servidor x Iteração')
    plt.legend()
    plt.grid(True)
    plt.show()    
  
  # Gráfico que combina tempo médio de espera, tempo médio de serviço e tempo médio ocioso do servidor
  def avg_times(self):
    wait_times, avg_wait_values = self.avg_wait_time()
    service_times, avg_service_values = self.avg_service_time()
    idle_times, avg_idle_values = self.avg_idle_server()
    num_iter = len(avg_wait_values)

    if num_iter == 0:
      return
    
    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(wait_times, avg_wait_values, color='brown', label='Tempo médio de espera', marker='o')
    plt.plot(service_times, avg_service_values, color='blue', label='Tempo médio de serviço', marker='o')
    if len(avg_idle_values):
      plt.plot(idle_times, avg_idle_values, color='magenta', label='Tempo médio ocioso do servidor', marker='o')
    plt.xlabel('Iteração')
    plt.ylabel('Tempo médio')
    plt.title('Tempo médio x Iteração')
    plt.legend()
    plt.grid(True)
    plt.show()

  # Gráfico da utilização do sistema
  def utilization(self):
    utilization = []
    total_service = 0

    for i, service_time in enumerate(self.mm1.service_times, start=1):
      total_service += service_time
      utilization.append(total_service / self.mm1.clock)
    
    return utilization
  
  def plot_utilization(self):
    utilization_values = self.utilization()
    num_iter = len(utilization_values)

    if num_iter == 0:
      return
    
    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(range(num_iter), utilization_values, color='blue', label='Simulado')
    plt.xlabel('Iteração')
    plt.ylabel('Utilização do sistema')
    plt.title('Utilização do sistema x Iteração')
    plt.legend()
    plt.grid(True)
    plt.show()

  # Probabilidade do servidor ficar ocioso
  def prob_idle_server():
    pass

  # Probabilidade do cliente esperar na fila
  def prob_wait_queue():
    pass

  # Imprime estatísticas da simulação
  def stats(self, num_customers, final_time):
    print(f'Número de clientes atendidos: {num_customers}')
    if (len(self.mm1.queue)):
      print(f'Número de clientes que permaneceram na fila: {len(self.mm1.queue)}')

    _, avg_wait = self.avg_wait_time()
    print(f'Tempo médio de espera: {avg_wait[-1]:.2f}')

    _, avg_service = self.avg_service_time()
    print(f'Tempo médio de serviço: {avg_service[-1]:.2f}')

    _, avg_idle = self.avg_idle_server()
    if len(avg_idle):
      print(f'Tempo médio ocioso do servidor: {avg_idle[-1]:.2f}')
    
    print(f'Tempo final da simulação: {final_time:.2f}')