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
  n_gens = 0 # Contador de gerações
  tot_sis_time = 0  # Tempo total no sistema

  # Gera o tempo da primeira infecção
  rand = random.random()
  t_next_infection = -math.log(rand) / infection_rate
  tot_lambda = t_next_infection

  # Inicio da simulacao
  # Instruções para a geração da distribuição offspring:
  # Dada uma chegada (infecção), é gerado o tempo de recuperação do indivíduo e,
  # a partir desse tempo, é gerado o número de indivíduos que foram infectados por
  # ele durante o seu tempo de recuperação
  # O critério de parada é quando o tempo de recuperação gerado for maior que
  # o tempo de chegada (infecção) gerado. Todos os indivíduos que foram gerados por
  # essa função correspondem a uma geração.
  while n_gens < N:
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

      # Chegada a um sistema vazio
      if n == 1:
        rand = random.random()
        t_mu = -math.log(rand) / recovery_rate
        t_next_recovery = clock + t_mu
        tot_mu += t_mu
      
      # Inicializa a primeira geração com o paciente 0 que chega no tempo 0
      if n_gens == 0:
        generations[n_gens] = [0]
        n_gens += 1
    
    # Evento de recuperação
    else:
      # Atualiza relogio e contadores
      clock = t_next_recovery
      n -= 1
      n_recovered += 1

      # Enquanto um individuo estiver em recuperação, este vai gerar novas
      # infecções, que serão os seus filhos e farão parte da mesma geração. Na
      # medida que essas novas infecções são geradas, elas são atendidas
      # imediatamente. Quando o tempo de recuperação do individuo atual for
      # maior que o tempo de chegada da nova infecção, a geração atual é
      # finalizada (ou seja, todos os individuos gerados, já foram atendidos/
      # recuperados) e o processo de geração de novas infecções é reiniciado
      while True:
        # Filhos do individuo que está em recuperação. Cada elemento da lista é
        # o clock na chegada de um novo individuo
        offspring = []
        t_child_next_infection = 0
        t_child_next_recovery = 0
        t_child_lambda = 0
        t_child_mu = 0

        # Gera um numero aleatorio de filhos de acordo com a distribuição Poisson
        num_children = np.random.poisson(infection_rate)
        for _ in range(num_children):
          # Gera uma nova infecção/chegada
          rand = random.random()
          t_child_lambda = -math.log(rand) / infection_rate
          t_child_next_infection = clock + t_child_lambda
          tot_lambda += t_child_lambda

          # Atualiza relogio e contadores
          clock = t_child_next_infection
          n += 1
          n_infected += 1

          # Adiciona o tempo de chegada do novo individuo na lista de filhos
          offspring.append(clock)

          # Gera tempo de recuperação
          rand = random.random()
          t_child_mu = -math.log(rand) / recovery_rate
          t_child_next_recovery = clock + t_child_mu
          tot_mu += t_child_mu
            
          # Atualiza relogio e contadores
          clock = t_child_next_recovery
          n -= 1
          n_recovered += 1

        # Se o tempo de recuperação do individuo atual for maior que o tempo de
        # chegada da nova infecção, a geração atual é finalizada e o processo de
        # geração de novas infecções é reiniciado. Enquanto isso não acontece,
        # novas infecções são geradas e atendidas imediatamente
        if t_next_recovery < t_child_next_infection:
          # Adiciona a geração atual no dicionário de gerações
          generations[n_gens] = offspring
          n_gens += 1
          # Atualiza tempos de infecção e recuperação
          t_next_infection = t_child_next_infection
          t_next_recovery = t_child_next_recovery
          break
  
  return {
    "clock": clock, # Tempo final de simulacao
    "generations": generations, # Dicionario de geracoes
  }

def main():
  N = 4
  infection_rate = 0.5
  recovery_rate = 1
  result = run_epidemy(N, infection_rate, recovery_rate)
  print(result["generations"])

if __name__ == "__main__":
  main()