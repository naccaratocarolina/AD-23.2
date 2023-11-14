import numpy as np
import datetime
import random

class mm1_epidemy:
  t_chegada = 0
  t_saida = 0

  # inicializacao da classe
  def __init__(
    self,
    num_sims=20,
    tx_chegada=1,
    tx_saida=1,
    max_iter=1000000,
    debug=False,
    name=None
  ):
    self.num_sims = num_sims
    self.tx_chegada = tx_chegada
    self.tx_saida = tx_saida
    self.max_iter = max_iter
    self.debug = debug

    # semenado para manter consistencia entre as simulacoes
    random.seed(43)

    # nome do arquivo de saida a partir do horario de execucao
    horario = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    self.out_file = (
      'mm1_epidemy.' +
      (name if name else '') +
      '.' + horario + '.json'
    )
  
  # funcoes geradoras de tempo
  def gera_chegada(self):
    self.t_chegada += np.random.exponential(1/self.tx_chegada)

  def gera_saida(self):
    self.t_saida += np.random.exponential(1/self.tx_saida)

  # funcao que decide qual evento acontece primeiro
  def next_event(self):
    if self.t_saida < self.t_chegada:
      return 'saida'
    else:
      return 'chegada'

  def run_one_mm1_epid(self):
    # tempos
    self.gera_chegada()
    self.gera_saida()

    # primeira geracao
    num_gen = 1

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

    while it < self.max_iter:
      if self.debug:
        print('====================================================')
        print(self.next_event())
        print('iteracao:', it)
        print('estou na geracao', num_gen)
        print('qtd. de pessoas na geracao atual', tam_gen)
        print('qtd. de pessoas na geracao anterior', tam_gen_ant)
        print('----------------------------------------------------')

      if self.next_event() == 'saida':

        # muda de pai
        qtd_filhos_arr.append(qtd_filhos)
        qtd_filhos_ant = qtd_filhos
        tam_gen += qtd_filhos
        qtd_filhos = 0

        # atendi mais um pai
        pais_atendidos += 1

        if self.debug:
          print('saiu um pai, agora tenho', pais_atendidos, 'pais atendidos')
          print('o pai que sai tem', qtd_filhos_ant, 'filhos')

        # troca de geracao depois de atender todos os pais
        if pais_atendidos == tam_gen_ant or tam_gen_ant == None:
          if self.debug:
            print('!! trocou de geracao !!')
          tam_gen_arr.append(tam_gen)
          tam_gen_ant = tam_gen
          pais_atendidos = 0
          tam_gen = 0
          qtd_filhos = 0
          num_gen += 1

        if (pais_atendidos == tam_gen_ant) and tam_gen == 0:
          if self.debug:
            print('!! extinçao !!')
          extinta = True
          break

        # gera proxima saida
        self.gera_saida()

      if self.next_event() == 'chegada':
        qtd_filhos += 1
        if self.debug:
          print('chegou um filho, agora tenho', qtd_filhos, 'filhos')

        # gera proxima chegada
        self.gera_chegada()

      it += 1
      if self.debug:
        print('====================================================')

    arr_aux = np.array(qtd_filhos_arr)
    freq = [0] * int(arr_aux.max() + 1)
    for i in range(len(freq)):
      freq[i] = (arr_aux == i).sum()

    dist = freq / sum(freq)

    print('Extinta?', extinta)
    print('Numero de geracoes:', num_gen)
    print('Numero de iteracoes:', it)
    print('Distri. de nascimentos:', dist)
    print('\n')

    # cria JSON de saida
    return {
      'extinta': extinta,
      'tam_ger_arr': tam_gen_arr,
      'qtd_filhos_arr': qtd_filhos_arr,
      'num_geracoes': num_gen,
      'num_iteracoes': it,
      'freq_nascimentos': freq,
      'dist_nascimentos': dist.tolist(),
    }

  def run_mm1_epid(self):
    # rodando N simulações
    out = {
      'num_sims': self.num_sims,
      'tx_chegada': self.tx_chegada,
      'tx_saida': self.tx_saida,
      'max_iter': self.max_iter,
      'debug': self.debug,
      'name': self.out_file,
      'sims': []
    }

    for i in range(self.num_sims):
      out['sims'].append(self.run_one_mm1_epid())

    terminam = 0
    duracao_periodo_ocupado = 0
    duracao_periodo_ocupado_global = 0
    media_freq_nascimentos = []
    grau_saida_raiz = 0
    grau_saida_maximo = 0
    altura_arvore = 0
    qnt_filhos_global = []

    # calcula algumas metricas
    for sim in out['sims']:
      if sim['extinta']:
        # periodos ocupados que terminam
        terminam += 1

        # duração do periodo ocupado
        duracao_periodo_ocupado += sim['num_iteracoes']
      
      # duração do periodo ocupado global
      duracao_periodo_ocupado_global += sim['num_iteracoes']

      # frequencia de nascimentos
      media_freq_nascimentos.append(sim['freq_nascimentos'])

      # grau de saida da raiz
      grau_saida_raiz += sim['qtd_filhos_arr'][0]

      # grau de saida maximo
      grau_saida_maximo += max(sim['qtd_filhos_arr'])

      # altura da arvore
      altura_arvore += sim['num_geracoes']

      # vetor que retorna a combinacao de todos os filhos de todos os pais de todas as simulacoes
      qnt_filhos_global.append(sim['qtd_filhos_arr'])

    # fraçao de periodos ocupados que terminam
    sim['frac_periodos_terminam'] = terminam / self.num_sims

    # media do tempo que a epidemia dura (apenas simulacoes que terminam)
    sim['media_duracao_epidemia'] = duracao_periodo_ocupado / terminam

    # media do tempo global que a epidemia dura (incluindo simulacoes que terminam e nao terminam)
    sim['media_duracao_epidemia_global'] = duracao_periodo_ocupado_global / self.num_sims
    
    # media da frequencia de nascimentos
    sim['media_freq_nascimentos'] =  np.array([sum(y) for y in zip(*media_freq_nascimentos)]).mean()

    # media do grau de saida da raiz
    sim['media_grau_saida_raiz'] = grau_saida_raiz / terminam

    # media do grau de saida maximo
    sim['media_grau_saida_maximo'] = grau_saida_maximo / terminam

    # media da altura da arvore
    sim['media_altura_arvore'] = altura_arvore / terminam
    
    # lista de filhos global
    qnt_filhos_global_ordenado = np.sort(np.concatenate(qnt_filhos_global))
    valores_unicos, frequencias = np.unique(qnt_filhos_global_ordenado, return_counts=True)
    probabilidades = []
    
    for i in frequencias:
      probabilidades.append(i / sum(frequencias))
    
    cdf_cum = np.cumsum(probabilidades)
    
    sim['cdf_valores_eixo_x'] = valores_unicos.tolist()
    sim['cdf_eixo_y'] = cdf_cum.tolist()

    # escreve JSON de saida
    with open('dados/'+self.out_file, 'w') as f:
      f.write(
        str(out)
        .replace('\'', '\"')
        .replace('False', 'false')
        .replace('True', 'true')
      )

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
