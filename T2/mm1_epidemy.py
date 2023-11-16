import json
import numpy as np
import datetime
import random

def calc_dist(arr):
  if len(arr) == 0:
    return []

  arr_aux = np.array(arr)
  freq = [0] * int(arr_aux.max() + 1)
  for i in range(len(freq)):
    freq[i] = (arr_aux == i).sum()

  dist = freq / sum(freq)
  return dist.tolist()

def calc_mean(arr):
  if len(arr) == 0:
    return 0
  return np.array(arr).mean().tolist()

def append(arr, obj):
  arr_ = arr.copy()
  # se o objeto é um array, concatena
  if isinstance(obj, list):
    return arr_ + obj
  # se o objeto é um número, caracter ou string, adiciona
  if isinstance(obj, (int, float, str)):
    arr_.append(obj)
  return arr_

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
    self.name = name

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

    arr_filhos_por_gen = [1]
    arr_filhos_por_pai = []

    pais_atendidos = 0

    # Acumulado de clientes atendidos na simulação (pais e filhos)
    acum_clientes = 0

    # geracao de cada no
    arr_gen_por_no = [0]

    # maximo de filhos de um pai
    max_qtd_filhos = 0

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
        max_qtd_filhos = max(max_qtd_filhos, qtd_filhos)
        arr_filhos_por_pai.append(qtd_filhos)
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
          acum_clientes += pais_atendidos
          if self.debug:
            print('!! trocou de geracao !!')
          arr_filhos_por_gen.append(tam_gen)
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
        # mais um filho
        qtd_filhos += 1

        # geracao do filho
        arr_gen_por_no.append(num_gen+1)

        if self.debug:
          print('chegou um filho, agora tenho', qtd_filhos, 'filhos')

        # gera proxima chegada
        self.gera_chegada()

      it += 1
      if self.debug:
        print('====================================================')

    arr_aux = np.array(arr_filhos_por_pai)
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
      'filhos_por_gen': arr_filhos_por_gen,
      'filhos_por_pai': arr_filhos_por_pai,
      'num_geracoes': num_gen,
      'num_iteracoes': it,
      'gen_por_no': arr_gen_por_no,
      'freq_nascimentos_por_pai': freq,
      'dist_nascimentos_por_pai': dist.tolist(),
      'num_max_filhos': max_qtd_filhos,
      'qnt_filhos_1_gen': arr_filhos_por_gen[1] if len(arr_filhos_por_gen) > 1 else 0,
      'acum_clientes': acum_clientes,
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
      print('Simulação', i)
      out['sims'].append(self.run_one_mm1_epid())

    ### iterar para cada simulação (separando em terminam e todas)
    ### acumular as métricas de cada simulação (separando em terminam e todas)
    metrics = {
      'terminam': {
        'qnt_filhos_por_pai': [],
        'qnt_filhos_raiz': [],
        'grau_saida_maximo': [],
        'qtd_geracoes': [],
        'gen_por_no': [],
        'qtd_iteracoes': [],
        'qtd_pais_atendidos': [],
      },
      'todas': {
        'qnt_filhos_por_pai': [],
        'qnt_filhos_raiz': [],
        'grau_saida_maximo': [],
        'qtd_geracoes': [],
        'gen_por_no': [],
        'qtd_iteracoes': [],
        'qtd_pais_atendidos': [],
      }
    }

    for sim in out['sims']:
      if sim['extinta']:
        metrics['terminam']['qnt_filhos_por_pai'] = append(metrics['terminam']['qnt_filhos_por_pai'], sim['filhos_por_pai'])
        metrics['terminam']['qnt_filhos_raiz'] = append(metrics['terminam']['qnt_filhos_raiz'], sim['qnt_filhos_1_gen'])
        metrics['terminam']['grau_saida_maximo'] = append(metrics['terminam']['grau_saida_maximo'], sim['num_max_filhos'])
        metrics['terminam']['qtd_geracoes'] = append(metrics['terminam']['qtd_geracoes'], sim['num_geracoes'])
        metrics['terminam']['gen_por_no'] = append(metrics['terminam']['gen_por_no'], sim['gen_por_no'])
        metrics['terminam']['qtd_iteracoes'] = append(metrics['terminam']['qtd_iteracoes'], sim['num_iteracoes'])
        metrics['terminam']['qtd_pais_atendidos'] = append(metrics['terminam']['qtd_pais_atendidos'], sim['acum_clientes'])
      metrics['todas']['qnt_filhos_por_pai'] = append(metrics['todas']['qnt_filhos_por_pai'], sim['filhos_por_pai'])
      metrics['todas']['qnt_filhos_raiz'] = append(metrics['todas']['qnt_filhos_raiz'], sim['qnt_filhos_1_gen'])
      metrics['todas']['grau_saida_maximo'] = append(metrics['todas']['grau_saida_maximo'], sim['num_max_filhos'])
      metrics['todas']['qtd_geracoes'] = append(metrics['todas']['qtd_geracoes'], sim['num_geracoes'])
      metrics['todas']['gen_por_no'] = append(metrics['todas']['gen_por_no'], sim['gen_por_no'])
      metrics['todas']['qtd_iteracoes'] = append(metrics['todas']['qtd_iteracoes'], sim['num_iteracoes'])
      metrics['todas']['qtd_pais_atendidos'] = append(metrics['todas']['qtd_pais_atendidos'], sim['acum_clientes'])

    # resultados (media entre as simulações)
    results = {
      'arquivo': self.out_file,
      'num_sims': self.num_sims,
      'tx_chegada': self.tx_chegada,
      'tx_saida': self.tx_saida,
      'max_iter': self.max_iter,
      'caso': self.name,
      'terminam': {},
      'todas': {},
    }

    ### • qual a distribuição dos graus de saída?
    ###   obs.: plote a CDF do grau de saída dos vértices
    results['terminam']['dist_grau_saida'] = calc_dist(metrics['terminam']['qnt_filhos_por_pai'])
    results['todas']['dist_grau_saida'] = calc_dist(metrics['todas']['qnt_filhos_por_pai'])
    ### • qual o grau médio de saída da raiz?
    results['terminam']['grau_medio_saida_raiz'] = calc_mean(metrics['terminam']['qnt_filhos_raiz'])
    results['todas']['grau_medio_saida_raiz'] = calc_mean(metrics['todas']['qnt_filhos_raiz'])
    ### • qual a média do grau de saída máximo?
    results['terminam']['grau_de_saida_maximo'] = calc_mean(metrics['terminam']['grau_saida_maximo'])
    results['todas']['grau_de_saida_maximo'] = calc_mean(metrics['todas']['grau_saida_maximo'])
    ### • qual a altura média da árvore?
    results['terminam']['altura_media'] = calc_mean(metrics['terminam']['qtd_geracoes'])
    results['todas']['altura_media'] = calc_mean(metrics['todas']['qtd_geracoes'])
    ### • qual a média das alturas dos nós das árvores?
    results['terminam']['altura_media_nos'] = calc_mean(metrics['terminam']['gen_por_no'])
    results['todas']['altura_media_nos'] = calc_mean(metrics['todas']['gen_por_no'])
    ### • qual a média da duração do período ocupado?
    results['terminam']['media_duracao_periodo_ocupado'] = calc_mean(metrics['terminam']['qtd_iteracoes'])
    results['todas']['media_duracao_periodo_ocupado'] = calc_mean(metrics['todas']['qtd_iteracoes'])
    ### • qual a média do número de clientes atendidos por período ocupado?
    results['terminam']['media_clientes_atendidos'] = calc_mean(metrics['terminam']['qtd_pais_atendidos'])
    results['todas']['media_clientes_atendidos'] = calc_mean(metrics['todas']['qtd_pais_atendidos'])

    # cria e exporta JSON de saida na pasta 'dados'
    with open('dados/'+self.out_file, 'w') as outfile:
      json.dump(results, outfile, indent=2, ensure_ascii=False)