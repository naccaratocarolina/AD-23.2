import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from public.common import *

class Stats():
  def __init__(self, mm1):
    self.mm1 = mm1 # Simulação MM1
    self.rho = mm1.arrival_rate / mm1.service_rate # Fator de utilização ρ = λ/μ
  
  def confidence_interval(self, data):
    n = len(data)
    mean = sum(data) / n
    std = np.std(data)
    h = std * 1.96 / np.sqrt(n)
    return [mean - h, mean + h]
  
  def avg_times(self, list_times):
    if len(list_times) == 0:
      return ([], [])

    times = []
    avg = []
    total = 0

    for i, (clock, time) in enumerate(list_times, start=1):
      total += time
      times.append(clock)
      avg.append(total / i)
    
    return (times, avg)

  def plot_graph(self, ax, avg_times, xlabel, ylabel, color):
    times, avg = avg_times
    num_iter = len(avg_times)

    if num_iter == 0:
      return
    
    # Plotar gráfico
    ax.plot(times, avg, color=color, label='Simulado')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(f'{ylabel} x {xlabel}')
    ax.legend()
    ax.grid(True)
  
  # Número médio analítico de pessoas na fila (Lei de Little)
  def avg_queue_len_analytic(self):
    if self.rho >= 1:
      return float('inf')
    return self.rho**2/(1 - self.rho)

  # Número médio simulado de pessoas na fila
  def avg_queue_len_sim(self):
    num_iter = len(self.mm1.queue_len)
    if num_iter == 0:
      return (0, [])

    queue_len = [e[1] for e in self.mm1.queue_len]
    total_queue_mean = 0

    # Calcula tamanho total medio da fila
    if self.mm1.queue:  # Verifica se a fila não está vazia
      final_queue_len = len(self.mm1.queue)
      total_queue_mean = (sum(queue_len) + final_queue_len) / (len(queue_len) + final_queue_len)
    else:
      total_queue_mean = sum(queue_len) / len(queue_len)
    
    avg_len = []
    queue_len_by_iter = 0
    
    # Calcula tamanho medio da fila por iteração
    for i, (_, queue_len) in enumerate(self.mm1.queue_len, start=1):
      queue_len_by_iter += queue_len
      avg_len.append(queue_len_by_iter / i)
    
    return (total_queue_mean, avg_len)    

  def plot_avg_queue_len(self, ax):
    # Calcular tamanho médio da fila simulado
    _, avg_len_values = self.avg_queue_len_sim()
    num_iter = len(avg_len_values)

    if num_iter == 0:
      return

    # Calcula intervalo de confiança
    ci = self.confidence_interval(avg_len_values)
    upper_ci = [avg + (ci[1] - ci[0]) / 2 for avg in avg_len_values]
    lower_ci = [avg - (ci[1] - ci[0]) / 2 for avg in avg_len_values]

    # Plotar gráfico
    times = range(num_iter)
    ax.plot(times, avg_len_values, color='green', label='Simulado')
    ax.plot(times, upper_ci, color='red', alpha=0.5, linestyle='dashed', label='Intervalo de confiança superior')
    ax.plot(times, lower_ci, color='red', alpha=0.5, linestyle='dashed', label='Intervalo de confiança inferior')
    ax.set_xlabel('Iteração')
    ax.set_ylabel('Número médio de pessoas na fila')
    ax.set_title('Número médio de pessoas na fila x Iteração')
    ax.legend()
    ax.grid(True)

  # Gráfico do tempo médio na fila de espera
  def avg_wait_time(self):
    return self.avg_times(self.mm1.wait_times)

  def plot_avg_wait_time(self, ax):
    self.plot_graph(ax, self.avg_wait_time(), 'Iteração', 'Tempo médio de espera', 'brown')

  # Gráfico do tempo médio de serviço
  def avg_service_time(self):
    return self.avg_times(self.mm1.service_times)

  def plot_avg_service_time(self, ax):
    self.plot_graph(ax, self.avg_service_time(), 'Iteração', 'Tempo médio de serviço', 'blue')

  # Gráfico do tempo médio ocioso do servidor
  def avg_idle_server(self):
    return self.avg_times(self.mm1.idle_times)

  def plot_avg_idle_server(self, ax):
    self.plot_graph(ax, self.avg_idle_server(), 'Iteração', 'Tempo médio ocioso do servidor', 'magenta')
  
  # Gráfico que combinado os gráficos de tempo médio de espera, tempo médio de
  # serviço e tempo médio ocioso do servidor
  def plot_global_avg(self, ax):
    wait_times, avg_wait = self.avg_wait_time()
    service_times, avg_service = self.avg_service_time()
    idle_times, avg_idle = self.avg_idle_server()
    
    # Combina os tempos, formando uma linha do tempo contínua
    times = list(set(wait_times + service_times + idle_times))
    times.sort()

    if len(avg_wait):
      ax.plot(wait_times, avg_wait, color='brown', label='Tempo médio de espera')

    if len(avg_service):
      ax.plot(service_times, avg_service, color='blue', label='Tempo médio de serviço')

    if len(avg_idle):
      ax.plot(idle_times, avg_idle, color='magenta', label='Tempo médio ocioso do servidor')

    ax.set_xlabel('Iteração')
    ax.set_ylabel('Tempo médio')
    ax.set_title('Tempo médio x Iteração')
    ax.legend()
    ax.grid(True)

  def prob_idle_server(self):
    # Simulado
    num_idle = len(self.mm1.idle_times)
    num_iter = len(self.mm1.queue_len)

    if num_iter == 0:
      return (0, 0)

    prob_idle_sim = num_idle / num_iter

    # Analítico
    prob_idle_analytic = float('inf')
    if self.rho < 1:
      prob_idle_analytic = 1 - self.rho
    
    return (prob_idle_sim, prob_idle_analytic)
  
  def prob_wait(self):
    # Simulado
    num_wait = len(self.mm1.wait_times)
    num_iter = len(self.mm1.queue_len)

    if num_iter == 0:
      return (0, 0)

    prob_wait_sim = num_wait / num_iter

    # Analítico
    prob_wait_analytic = self.rho

    return (prob_wait_sim, prob_wait_analytic)

  def avg_respose_time(self):
    # Simulado
    _, avg_wait = self.avg_wait_time()
    _, avg_service = self.avg_service_time()
    avg_res_sim = 0
    if len(avg_wait) and len(avg_service):
      avg_res_sim = avg_wait[-1] + avg_service[-1]
    else:
      return (0, 0)

    # Analítico
    avg_res_analytic = float('inf')
    if self.rho < 1:
      avg_res_analytic = (1/self.mm1.service_rate) / (1 - self.rho)

    return (avg_res_sim, avg_res_analytic)

  def plot_all(self):
    # Cria a figura com o grid principal
    fig = plt.figure(figsize=(15, 11))

    # Grids
    gs_main = fig.add_gridspec(2, 1, hspace=0.5)
    gs_sup = gs_main[0].subgridspec(1, 2)
    gs_inf = gs_main[1].subgridspec(1, 3)

    # Gráfico combinado
    self.plot_global_avg(fig.add_subplot(gs_sup[0]))

    # Gráfico do número médio de pessoas na fila
    self.plot_avg_queue_len(fig.add_subplot(gs_sup[1]))

    # Gráfico do tempo médio na fila de espera
    self.plot_avg_wait_time(fig.add_subplot(gs_inf[0]))

    # Gráfico do tempo médio de serviço
    self.plot_avg_service_time(fig.add_subplot(gs_inf[1]))

    # Gráfico do tempo médio ocioso do servidor
    self.plot_avg_idle_server(fig.add_subplot(gs_inf[2]))

    fig.suptitle('Estatísticas da simulação', fontsize=20)
    plt.subplots_adjust()
    plt.show()

  # Imprime estatísticas da simulação
  def stats(self, num_customers, final_time):
    # Total de clientes atendidos e que permaneceram na fila
    print(f'Número de clientes atendidos: {STATS_COLOR}{num_customers}{RESET_COLOR}')
    if (len(self.mm1.queue)):
      print(f'Número de clientes que permaneceram na fila: {STATS_COLOR}{len(self.mm1.queue)}{RESET_COLOR}')
    
    # Número médio de clientes na fila (Simulado e analítico)
    avg_clients, _ = self.avg_queue_len_sim()
    avg_clients_analytic = self.avg_queue_len_analytic()
    if avg_clients > 0:
      print('Número médio de clientes na fila:')
      print(f'  {BOLD}Simulado{RESET_COLOR}: {STATS_COLOR}{avg_clients:.2f}{RESET_COLOR}')
      print(f'  {BOLD}Analítico{RESET_COLOR}: {STATS_COLOR}{avg_clients_analytic:.2f}{RESET_COLOR}')

    # Tempo médio de espera
    _, avg_wait = self.avg_wait_time()
    if self.rho < 1:
      avg_wait_analytic = self.rho / (self.mm1.service_rate * (1 - self.rho))
    else:
      avg_wait_analytic = float('inf')
    if len(avg_wait):
      print(f'Tempo médio de espera:')
      print(f'  {BOLD}Simulado{RESET_COLOR}: {STATS_COLOR}{avg_wait[-1]:.2f}{RESET_COLOR}')
      print(f'  {BOLD}Analítico{RESET_COLOR}: {STATS_COLOR}{avg_wait_analytic:.2f}{RESET_COLOR}')

    # Tempo médio de serviço
    _, avg_service = self.avg_service_time()
    if len(avg_service):
      print(f'Tempo médio de serviço: {STATS_COLOR}{avg_service[-1]:.2f}{RESET_COLOR}')

    # Tempo médio ocioso do servidor
    _, avg_idle = self.avg_idle_server()
    if len(avg_idle):
      print(f'Tempo médio ocioso do servidor: {STATS_COLOR}{avg_idle[-1]:.2f}{RESET_COLOR}')
    
    # Tempo médio de resposta (Simulado e analítico)
    avg_res_sim, avg_res_analytic = self.avg_respose_time()
    print('Tempo médio de resposta:')
    print(f'  {BOLD}Simulado{RESET_COLOR}: {STATS_COLOR}{avg_res_sim:.2f}{RESET_COLOR}')
    print(f'  {BOLD}Analítico{RESET_COLOR}: {STATS_COLOR}{avg_res_analytic:.2f}{RESET_COLOR}')

    # Probabilidade de o servidor ficar ocioso (Simulado e analítico)
    prob_idle_sim, prob_idle_analytic = self.prob_idle_server()
    print('Probabilidade de o servidor ficar ocioso:')
    print(f'  {BOLD}Simulado{RESET_COLOR}: {STATS_COLOR}{prob_idle_sim:.2f}{RESET_COLOR}')
    print(f'  {BOLD}Analítico{RESET_COLOR}: {STATS_COLOR}{prob_idle_analytic:.2f}{RESET_COLOR}')

    # Probabilidade de o cliente ter que esperar (Simulado e analítico)
    prob_wait_sim, prob_wait_analytic = self.prob_wait()
    print('Probabilidade de o cliente ter que esperar:')
    print(f'  {BOLD}Simulado{RESET_COLOR}: {STATS_COLOR}{prob_wait_sim:.2f}{RESET_COLOR}')
    print(f'  {BOLD}Analítico{RESET_COLOR}: {STATS_COLOR}{prob_wait_analytic:.2f}{RESET_COLOR}')

    # Tempo final da simulação
    print(f'Tempo final da simulação: {STATS_COLOR}{final_time:.2f}{RESET_COLOR}')

    # Gráficos
    self.plot_all()