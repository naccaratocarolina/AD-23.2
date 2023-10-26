import random
import math
import numpy as np

INF = math.inf # Valor "infinito"

def run_mm1(arrival_rate, service_rate):
  random.seed()
  seed = 0  # Variavel para numeros aleatórios

  N = 2000  # Numero total de clientes a serem atendidos
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

  seed = random.random()
  t_a = -math.log(seed) / arrival_rate
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
      seed = random.random()
      t_lambda = -math.log(seed) / arrival_rate
      t_a = clock + t_lambda
      tot_lambda += t_lambda

      # Chegada a um sistema vazio
      if n == 1:
        seed = random.random()
        t_mu = -math.log(seed) / service_rate
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
        seed = random.random()
        t_mu = -math.log(seed) / service_rate
        t_d = clock + t_mu
        tot_mu += t_mu

  # Tempo de espera para o cliente 2001
  return tot_sis_time

if __name__ == "__main__":
  arrival_rate = 0.5
  service_rate = 1

  valores_obtidos = []

  for i in range(200):
    valores_obtidos.append(run_mm1(arrival_rate, service_rate))

  # Calcular media e desvio padrao dos valores obtidos
  media = np.mean(valores_obtidos)
  desvio_padrao = np.std(valores_obtidos, ddof=1)  # ddof=1 para calcular o desvio padrao amostral

  # Numero de simulacões
  n = len(valores_obtidos)

  # Nivel de confianca
  confianca = 0.95

  # Calcular o erro padrao da media
  erro_padrao = desvio_padrao / np.sqrt(n)

  # Calcular o intervalo de confianca
  z = 1.96  # Valor critico para um nivel de confianca de 95%
  limite_inferior = media - z * erro_padrao
  limite_superior = media + z * erro_padrao

  # Valor analitico
  E_X = 1 / service_rate  # Valor medio do servico
  valor_analitico = E_X / (1 - arrival_rate * E_X)

  # Imprimir resultados
  print(f"Média dos valores obtidos: {media}")
  print(f"Desvio padrao dos valores obtidos: {desvio_padrao}")
  print(f"Intervalo de confiança (95%): ({limite_inferior}, {limite_superior})")
  print(f"Valor analítico: {valor_analitico}")