import random
import math
import numpy as np
import matplotlib.pyplot as plt

INF = math.inf

def run_epidemic_mm1(N, infection_rate, recovery_rate):
  # Fixar a semente do gerador de números aleatórios
  random.seed(10)

  l = 0 # Número pessoas no sistema
  n_infections = 0 # Contador de infecções
  n_recoveries = 0 # Contador de recuperacoes

  clock = 0 # Relógio de simulação
  t_next_inf = 0 # Instante do próximo evento de infecção
  t_next_rec = INF # Instante do próximo evento de recuperação

  t_between_inf = 0 # Tempo entre infecções
  t_between_rec = INF # Tempo entre recuperações

  sum_between_inf = 0 # Soma dos tempos entre infecções
  sum_between_rec = 0 # Soma dos tempos entre recuperações

  generations = [0] * (N+1) # Vetor onde a chave é a geração e o valor é o tamanho da mesma
  curr_gen = 0 # Geração atual
  curr_gen_size = 1 # Tamanho da geração atual

  it = 0 # Iteração atual

  # Loop principal da simulação
  while it < N:
    it += 1

    # Evento de infecção
    if t_next_inf < t_next_rec:
      clock = t_next_inf
      l += 1
      n_infections += 1
      generations[curr_gen + 1] += 1

      t_between_inf = random.expovariate(infection_rate)
      t_next_inf = clock + t_between_inf
      sum_between_inf += t_between_inf

      if l == 1:
        t_between_rec = random.expovariate(recovery_rate)
        t_next_rec = clock + t_between_rec

    # Evento de recuperação
    else:
      clock = t_next_rec
      l -= 1
      n_recoveries += 1
      curr_gen_size -= 1

      if l > 0:
        t_between_rec = random.expovariate(recovery_rate)
        t_next_rec = clock + t_between_rec
        sum_between_rec += t_between_rec

      else:
        break

      if curr_gen_size == 0:
        curr_gen += 1
        curr_gen_size = generations[curr_gen]

  return {
    'n_infections': n_infections,
    'n_recoveries': n_recoveries,
    'sum_between_inf': sum_between_inf,
    'sum_between_rec': sum_between_rec,
    'generations': generations,
    'number_of_generations': curr_gen,
    'clock': clock,
  }
  

def main():
  N = 10000  # Número total iterações
  infection_rate = 2.45  # Taxa média de infecção
  recovery_rate = 0.19  # Taxa média de recuperação
  result = run_epidemic_mm1(N, infection_rate, recovery_rate)

  print('Número de infeccoes:', result['n_infections'])
  print('Número de recuperacoes:', result['n_recoveries'])
  print('Tempo médio entre infeccoes:', result['sum_between_inf'] / result['n_infections'])
  print('Tempo médio entre recuperacoes:', result['sum_between_rec'] / result['n_recoveries'])
  print('Tempo médio de permanência:', result['clock'] / result['n_recoveries'])
  print('Tamanho médio das gerações:', np.mean(result['generations']))
  print('Número de gerações:', result['number_of_generations'])

if __name__ == "__main__":
  main()
