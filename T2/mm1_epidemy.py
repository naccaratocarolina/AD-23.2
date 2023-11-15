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

    # qtd. de filhos da 1a geração
    qnt_filhos_1_gen = 0

    # Acumulado de clientes atendidos na simulação (pais e filhos)
    acum_clientes = 0

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
          acum_clientes += tam_gen
          if num_gen == 1:
            qnt_filhos_1_gen = qtd_filhos_ant
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
      'max_qtd_filhos': arr_aux.max(),
      'qnt_filhos_1_gen': qnt_filhos_1_gen,
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
      out['sims'].append(self.run_one_mm1_epid())

    terminam = 0

    # 1) e 6) Duração do periodo ocupado
    duracao_periodo_ocupado = []

    # 2) Qnt. de filhos
    qnt_filhos_global = []
    qnt_filhos_terminam = []

    # 3) Lista da qnt. de filhos da 1a geração
    qnt_filhos_1_gen_terminam = []

    # 4) Lista da qnt. maxima de filhos
    qnt_max_filhos_terminam = []

    # 5) Lista da qnt. de geracoes
    qnt_gen_terminam = []

    # 7) Lista do acumulado de clientes atendidos
    acum_clientes_global = []
    acum_clientes_terminam = []

    # calcula algumas metricas
    for sim in out['sims']:
      if sim['extinta']:
        # periodos ocupados que terminam
        terminam += 1

        # 1) e 6) Duração do periodo ocupado das simulações que terminam
        duracao_periodo_ocupado.append(sim['num_iteracoes'])

        # 2) Qnt. de filhos das simulações que terminam
        qnt_filhos_terminam.append(sim['qtd_filhos_arr'])

        # 3) Lista da qnt. de filhos da 1a geração das simulações que terminam
        qnt_filhos_1_gen_terminam.append(sim['qnt_filhos_1_gen'])

        # 4) Lista da qnt. maxima de filhos das simulações que terminam
        qnt_max_filhos_terminam.append(sim['max_qtd_filhos'])

        # 5) Lista da qnt. de geracoes das simulações que terminam
        qnt_gen_terminam.append(sim['num_geracoes'])

        # 7) Lista do acumulado de clientes atendidos das simulações que terminam
        acum_clientes_terminam.append(sim['acum_clientes'])

      # 2) Qnt. de filhos de todas as simulações
      qnt_filhos_global.append(sim['qtd_filhos_arr'])

      # 7) Lista do acumulado de clientes atendidos por simulação
      acum_clientes_global.append(sim['acum_clientes'])

    # 1) Distribuicao do tempo que a epidemia dura
    duracao_terminam_ordernado = np.sort(np.array(duracao_periodo_ocupado))
    valores_unicos_terminam, frequencias_terminam = np.unique(duracao_terminam_ordernado, return_counts=True)

    sim['duracao_terminam'] = valores_unicos_terminam.tolist()
    sim['freq_duracao_terminam'] = frequencias_terminam.tolist()

    probabilidades_terminam = [i / sum(frequencias_terminam) for i in frequencias_terminam]
    cdf_cum_terminam = np.cumsum(probabilidades_terminam)

    sim['cdf_duracao_terminam_eixo_x'] = valores_unicos_terminam.tolist()
    sim['cdf_duracao_terminam_eixo_y'] = cdf_cum_terminam.tolist()

    # 2) Distribuicao da qtd. de filhos
    qnt_filhos_global_ordenado = np.sort(np.concatenate(qnt_filhos_global))
    valores_unicos, frequencias = np.unique(qnt_filhos_global_ordenado, return_counts=True)
    
    sim['filhos_gerados'] = valores_unicos.tolist()
    sim['freq_nascimentos'] = frequencias.tolist()
    
    probabilidades = [i / sum(frequencias) for i in frequencias]
    cdf_cum = np.cumsum(probabilidades)
    
    sim['cdf_valores_eixo_x'] = valores_unicos.tolist()
    sim['cdf_eixo_y'] = cdf_cum.tolist()

    # Media da frequencia de nascimentos
    sim['media_freq_nascimentos'] = np.array(frequencias).mean()

    # 3) Media da qnt. de filhos da 1a geracao (grau medio de saida da raiz)
    sim['grau_medio_saida_raiz_terminam'] = np.array(qnt_filhos_1_gen_terminam).mean()

    # 4) Media entre o maior numero de filhos por simulação (grau de saida maximo)
    sim['grau_de_saida_maximo_terminam'] = np.array(qnt_max_filhos_terminam).mean()

    # 5) Media da qnt de geracoes por simulação
    sim['altura_media_terminam'] = np.array(qnt_gen_terminam).mean()

    # 6) Media da duração do periodo ocupado
    sim['media_duracao_epidemia_terminam'] = np.array(duracao_periodo_ocupado).mean()

    # 7) Media do acumulado de clientes atendidos
    sim['media_acum_clientes_global'] = np.array(acum_clientes_global).mean()
    sim['media_acum_clientes_terminam'] = np.array(acum_clientes_terminam).mean()

    # Media das alturas dos nos das arvores ??????
    # TODO

    # Media entre o tamanho das "subarvores" geradas entre as extinções ??????
    # TODO

    # Escreve JSON de saida
    with open('dados/'+self.out_file, 'w') as f:
      f.write(
        str(out)
        .replace('\'', '\"')
        .replace('False', 'false')
        .replace('True', 'true')
      )
