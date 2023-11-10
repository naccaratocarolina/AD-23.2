import random
import math
import numpy as np

INF = math.inf # Valor "infinito"

# N: Número total de indivíduos infectados (ou seja, numero maximo de gerações)
# infection_rate: Taxa média de infecção (equivalente a taxa media de chegadas)
# recovery_rate: Taxa média de recuperação (equivalente a taxa media de serviço)
def run_epidemy(N, infection_rate, recovery_rate):
  # random.seed(10) # Descomente para fixar a semente
  rand = 0  # Variavel para numeros aleatórios

  n = 0  # Contador de indivíduos no sistema
  n_infected = 0  # Contador de indivíduos infectados
  n_recovered = 0  # Contador de indivíduos recuperados

  clock = 0  # Relógio interno
  t_next_infection = 0  # Próxima infecção agendada (clock + t_lambda)
  t_next_recovery = INF  # Próxima recuperação agendada (clock + t_mu)
  t_lambda = 0  # Tempo entre infecções gerado
  t_mu = 0  # Tempo de recuperação gerado
  tot_lambda = 0  # Total dos tempos entre infecções
  tot_mu = 0  # Total dos tempos de recuperação

  generations = {} # Dicionário de gerações: {geração: [tempos de infecção (chegada) de cada indivíduo da mesma geração]}
  children = {} # Dicionário de filhos por geração: {geração: [número de filhos gerados por cada pai pertencente a mesma geração]}
  n_gens = 1 # Contador de gerações
  n_offspring = 0 # Variavel auxiliar para troca de geração

  # Gera o tempo do paciente 0 que chegou no tempo 0 e gerou 0 filhos
  generations[0] = [0]
  children[0] = [0]

  # Gera o tempo da primeira infecção
  rand = random.random()
  t_next_infection = -math.log(rand) / infection_rate
  tot_lambda = t_next_infection

  # Inicio da simulacao
  it = 0
  # while it < 10:
  while n_gens < N:
  # while True:
    it += 1

    # Evento de infecção
    if t_next_infection < t_next_recovery:
      # Atualiza relogio e contadores
      clock = t_next_infection
      n += 1
      n_infected += 1

      # Gera proxima infecção/chegada
      rand = random.random()
      t_lambda = -math.log(rand) / infection_rate
      t_next_infection = clock + t_lambda
      tot_lambda += t_lambda

      # Adiciona tempo de infecção/chegada
      if n_gens not in generations:
        generations[n_gens] = []
      generations[n_gens].append(t_next_infection)

      # Chegada a um sistema vazio
      if n == 1 or t_next_recovery == INF:
        rand = random.random()
        t_mu = -math.log(rand) / recovery_rate
        t_next_recovery = clock + t_mu
        tot_mu += t_mu
    
    # Evento de recuperação
    else:
      # Atualiza relogio e contadores
      clock = t_next_recovery
      n -= 1
      n_recovered += 1

      # Troca de geração
      if n_offspring == n_recovered:
        if n_gens not in children:
          children[n_gens] = []
        n_gens += 1
        n_offspring = 0

      # Enquanto um individuo estiver em recuperação, este vai gerar novas
      # infecções, que serão os seus filhos e farão parte da mesma geração.
      # Quando o tempo de recuperação do individuo atual for maior que o
      # acumulado dos tempos de chegadas da nova infecção, a geração de
      # filhos deste individuos encerra
      elapsed_time = 0
      n_children = 0
      while elapsed_time < t_mu:
        n_children += 1

        # Atualiza relogio e contadores
        n += 1
        n_infected += 1

        # Gera uma infecção/filho
        rand = random.random()
        t_lambda = -math.log(rand) / infection_rate
        t_next_infection = clock + t_lambda
        tot_lambda += t_lambda

        if n_gens not in generations:
          generations[n_gens] = []
        generations[n_gens].append(t_next_infection)

        n_offspring += 1
        elapsed_time += t_lambda
      
      # Se o indiduo atual não gerou nenhum filho, adiciona 0 ao dicionario
      if n_gens not in children:
        children[n_gens] = []
      children[n_gens].append(n_children)

      # Atualiza relogio com o tempo de infecção do ultimo filho gerado
      clock = t_next_infection

      # Gera proxima recuperação/saída ou, se não houver mais indivíduos no
      # sistema, força proximo evento ser uma infecção/chegada
      if n == 0:
        t_next_recovery = INF
      else:
        rand = random.random()
        t_mu = -math.log(rand) / recovery_rate
        t_next_recovery = clock + t_mu
        tot_mu += t_mu

    # Se o numero de individuos no sistema for zero e a geração anterior não tiver
    # nenhum individuo, então a epidemia acabou
    if n == 0 and generations[n_gens - 1] == []:
      print('Extinção')
      break

  return {
    "clock": clock, # Tempo final de simulacao
    "generations": generations, # Dicionario de geracoes,
    "children": children, # Dicionario de filhos por geracao
  }

def main():
  N = 2
  infection_rate = 1
  recovery_rate = 20
  result = run_epidemy(N, infection_rate, recovery_rate)
  print('Gerações: ', result["generations"])
  print('Filhos: ', result["children"])
  print('Tempo final de simulação:', result["clock"])

if __name__ == "__main__":
  main()