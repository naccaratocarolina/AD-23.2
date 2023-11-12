import numpy as np
import random

# debug var
debug = False

# max iteracoes
max_iter = 100000

# random seed
random.seed(10)

# taxas
tx_chegada = 1.5
tx_saida = 0.2

t_chegada = 0
t_saida = 0

# funcoes geradoras de tempo
def gera_chegada(t_chegada):
  return t_chegada + np.random.exponential(1/tx_chegada)

def gera_saida(t_saida):
  return t_saida + np.random.exponential(1/tx_saida)

def next_event():
  if t_saida < t_chegada:
    return 'saida'
  else:
    return 'chegada'

def criterio_parada(tam_ger_arr, excesso=0.002):
  # caso a geracao esteja crescendo numa taxa muito alta, paramos
  # para saber se esta crescendo, usamos as ultimas 3 geracoes
  # e comparamos a taxa de crescimento com a taxa de chegadas
  excesso = 1 + excesso
  media = tx_chegada / tx_saida
  
  if len(tam_ger_arr) < 4:
    return False
  else:
    ult = tam_ger_arr[-1]
    penult = tam_ger_arr[-2]
    antpenult = tam_ger_arr[-3]

    if (
      ult > penult*media*excesso and
      penult > antpenult*media*excesso
    ):
      return True

    return False

# tempos
t_chegada = gera_chegada(t_chegada)
t_saida = gera_saida(t_saida)

# primeira geracao
num_gen = 1

# preciso servir esse 1 cara
qtd_pais_para_atender = 1

qtd_filhos = 0
qtd_filhos_ant = 1

# o proprio cara
tam_gen = 0
tam_gen_ant = None

tam_gen_arr = [1]
qtd_filhos_arr = []

pais_atendidos = 0

it = 0

extinta = False

while it < max_iter and not criterio_parada(tam_gen_arr):
  if debug:
    print('====================================================')
    print(next_event())
    print('iteracao:', it)
    print('estou na geracao', num_gen)
    print('qtd. de pessoas na geracao atual', tam_gen)
    print('qtd. de pessoas na geracao anterior', tam_gen_ant)
    print('----------------------------------------------------')

  if next_event() == 'saida':

    # muda de pai
    qtd_filhos_arr.append(qtd_filhos)
    qtd_filhos_ant = qtd_filhos
    tam_gen += qtd_filhos
    qtd_filhos = 0

    # atendi mais um pai
    pais_atendidos += 1

    if debug:
      print('saiu um pai, agora tenho', pais_atendidos, 'pais atendidos')
      print('o pai que sai tem', qtd_filhos_ant, 'filhos')

    # troca de geracao depois de atender todos os pais
    if pais_atendidos == tam_gen_ant or tam_gen_ant == None:
      if debug:
        print('!! trocou de geracao !!')
      tam_gen_arr.append(tam_gen)
      tam_gen_ant = tam_gen
      pais_atendidos = 0
      tam_gen = 0
      qtd_filhos = 0
      num_gen += 1

    if (pais_atendidos == tam_gen_ant) and tam_gen == 0:
      if debug:
        print('!! extinçao !!')
      extinta = True
      break
    
    # gera proxima saida
    t_saida = gera_saida(t_saida)

  if next_event() == 'chegada':
    qtd_filhos += 1
    if debug:
      print('chegou um filho, agora tenho', qtd_filhos, 'filhos')

    # gera proxima chegada
    t_chegada = gera_chegada(t_chegada)

  it += 1
  if debug:
    print('====================================================')

arr_aux = np.array(qtd_filhos_arr)
freq = [0] * int(arr_aux.max() + 1)
for i in range(len(freq)):
  freq[i] = (arr_aux == i).sum()

dist = freq / sum(freq)

print('Tamanho da geracao:', tam_gen_arr)
print('Quantidade de filhos:', qtd_filhos_arr)
print('Numero de geracoes:', num_gen)
print('Numero de iteracoes:', it)
print('Freq. de nascimentos:', freq)
print('Distri. de nascimentos:', dist)

# TODO: encapsular para rodar N simulaçõe

# RESULTADOS:
    ### fraçao de periodos ocupados que terminam
    ### tem que remover simulações infitas
# 1) média de tempo que a epidemia dura entre as N sim.
    ### distribuição dos graus de saida
# 2) achar a media do arr de distribuicao e plotar a CDF com ele
#    pra ficar legal, plotar todas as CDFs de tds. os 4 casos de teste juntas
#    acumulação das inversas de cada coord. do arr de dist.
    ### grau medio da saida da raiz
# 3) média da qtd. de pessoas da 1a geração (filhos da raiz) entre
#    as N simulações
    ### media do grau de saida maximo
# 4) média entre o maior numero de filhos de um pai entre as
#    N simulações (arr_aux.max())
    ### altura media da arvore
# 5) media entre a qtd de gerações entre todas as N simulações
#    array com todos os len(num_gen) e media desse array
    ### media das alturas dos nós das arvores
# 6) TEMOS QUE PENSAR NISSO
    ### media de duração do periodo ocupado
# 7) caso finito em que há extinsão, isso não faz muito sentido
#    no caso infinito, teremos que gerar uma nova chegada quando
#    a ultima geração for extinta
    ### media do numero de clientes por periodo ocupado
# 8) media entre o tamanho das "subarvores" geradas entre as extinções


