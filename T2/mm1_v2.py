import random
import math
import numpy as np

INF = math.inf # Valor "infinito"

# N: Numero total de clientes a serem atendidos
# arrival_rate: Taxa media de chegada
# service_rate: Taxa media de servico
def run_mm1(N, arrival_rate, service_rate):
  random.seed(10)
  rand = 0  # Variavel para numeros aleatórios

  n = 0  # Contador de clientes no sistema
  n_a = 0  # Contador de chegadas
  n_d = 0  # Contador de saidas

  clock = 0  # Relógio interno
  t_a = 0  # Próxima chegada agendada (clock + t_lambda)
  t_d = INF  # Próxima saida agendada (clock + t_mu)
  t_lambda = 0  # Tempo entre chegadas gerado
  t_mu = 0  # Tempo de servico gerado
  tot_lambda = 0  # Total dos tempos entre chegadas
  tot_mu = 0  # Total dos tempos de servico
  
  L = [0] * (N + 1)  # Vetor de tempos de chegada
  tot_sis_time = 0  # Tempo total no sistema

  rand = random.random()
  t_a = -math.log(rand) / arrival_rate
  tot_lambda = t_a

  # Inicio da simulacao
  while n_d < N:
    # Evento de chegada
    if t_a < t_d:
      clock = t_a
      n += 1
      n_a += 1
      if n_a <= N:
        L[n_a] = clock
      rand = random.random()
      t_lambda = -math.log(rand) / arrival_rate
      t_a = clock + t_lambda
      tot_lambda += t_lambda

      # Chegada a um sistema vazio
      if n == 1:
        rand = random.random()
        t_mu = -math.log(rand) / service_rate
        t_d = clock + t_mu
        tot_mu += t_mu
    
    # Evento de saida
    else:
      clock = t_d
      n -= 1
      n_d += 1
      tot_sis_time = clock - L[n_d]

      if n == 0:
        t_d = INF
      else:
        rand = random.random()
        t_mu = -math.log(rand) / service_rate
        t_d = clock + t_mu
        tot_mu += t_mu

  return {
    "tot_sis_time": tot_sis_time, # Tempo total no sistema do ultimo cliente
    "clock": clock, # Tempo final de simulacao
  }

def main():
  N = 2000  # Número total de clientes a serem atendidos
  arrival_rate = 0.5  # Taxa média de chegada
  service_rate = 1  # Taxa média de serviço
  result = run_mm1(N, arrival_rate, service_rate)
  print("Tempo total no sistema do último cliente:", result["tot_sis_time"])
  print("Tempo final de simulação:", result["clock"])

if __name__ == "__main__":
    main()
