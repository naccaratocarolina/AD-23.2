import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import glob
from mm1_epidemy import mm1_epidemy
import pandas as pd
from matplotlib.font_manager import FontProperties

# Caso 1: 
epidemia_caso1 = mm1_epidemy(
  tx_chegada=2,
  tx_saida=1,
  name='caso1'
)

# Caso 2:
epidemia_caso2 = mm1_epidemy(
  tx_chegada=4,
  tx_saida=2,
  name='caso2'
)

# Caso 3:
epidemia_caso3 = mm1_epidemy(
  tx_chegada=1,
  tx_saida=1.05,
  name='caso3'
)

# Caso 4:
epidemia_caso4 = mm1_epidemy(
  tx_chegada=1,
  tx_saida=1.10,
  name='caso4'
)

# Roda as simulacoes
# epidemia_caso1.run_mm1_epid()
# epidemia_caso2.run_mm1_epid()
# epidemia_caso3.run_mm1_epid()
# epidemia_caso4.run_mm1_epid()

def plot_cdf(tx_chegada, tx_saida, eixo_x, eixo_y, title, xlabel, ylabel, arquivo, prefixo, sufixo):
  if (len(eixo_x) <= 1):
    print(f'Não há dados suficientes para gerar o gráfico de {arquivo}!')
    return

  # Extrai caso do nome do arquivo
  caso = arquivo.split('.')[1]
  nome_arquivo = arquivo.replace('dados/', '').replace('.json', '')

  # Gera grafico da CDF
  plt.figure(figsize=(8, 6))
  plt.title(f'{title} {caso}: λ={tx_chegada}, μ={tx_saida}')

  # Interpolação linear
  f = interp1d(eixo_x, eixo_y, kind='linear')
  eixo_x_interp = np.linspace(min(eixo_x), max(eixo_x), num=1000, endpoint=True)
  eixo_y_interp = np.array(f(eixo_x_interp))

  plt.plot(eixo_x_interp, eixo_y_interp, label='CDF contínua')
  plt.step(eixo_x, eixo_y, label='CDF discreta', where='post', linestyle='--', color='red', alpha=0.5)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ticklabel_format(style='plain', axis='x')
  plt.legend()
  plt.savefig(f'graficos/{prefixo}_{nome_arquivo}_{sufixo}.png')
  plt.close()
  print(f'Gráfico {nome_arquivo}.png gerado com sucesso!')
  # plt.show()

# Estrutura de data:
# { title1: [value1], title2: [value2], ... }
def plot_table(data):
  df = pd.DataFrame(data)
  casos = ['Caso 1', 'Caso 2', 'Caso 3', 'Caso 4']
  df.insert(0, 'Caso', casos)
  plt.figure(figsize=(20, 10))
  plt.axis('off')
  table = plt.table(
    cellText=df.values,
    colLabels=df.columns,
    loc='center',
    cellLoc='center'
  )
  table.auto_set_font_size(False)
  table.set_fontsize(13)
  table.scale(1, 5)

  for (i, j), cell in table.get_celld().items():
    if i == 0 or j == 0:
      # Fonte em negrito
      cell.set_text_props(fontproperties=FontProperties(weight='bold'))
  
  plt.savefig('graficos/tabela.png')
  plt.close()
  print('Tabela gerada com sucesso!')

# Dados para a tabela
grau_medio_saida_raiz = []
grau_de_saida_maximo = []
altura_media = []
media_duracao_epidemia = []
media_acum_clientes = []

# Abre todos os arquivos na pasta dados
arquivos = glob.glob("dados/*.json")
for i, arquivo in enumerate(glob.glob("dados/*.json")):
  # Abre o arquivo JSON
  with open(arquivo) as f:
    dados_json = json.load(f)
    tx_chegada = dados_json['tx_chegada']
    tx_saida = dados_json['tx_saida']
    dados_sim = dados_json['sims'][-1]

    # Preenche listas da tabela
    grau_medio_saida_raiz.append(round(dados_sim['grau_medio_saida_raiz_terminam'], 3))
    grau_de_saida_maximo.append(round(dados_sim['grau_de_saida_maximo_terminam'], 3))
    altura_media.append(round(dados_sim['altura_media_terminam'], 3))
    media_duracao_epidemia.append(round(dados_sim['media_duracao_epidemia_terminam'], 3))
    media_acum_clientes.append(round(dados_sim['media_acum_clientes_terminam'], 3))

    # CDF distribuicao de tempo (epidemias que terminam)
    plot_cdf(
      tx_chegada,
      tx_saida,
      dados_sim['cdf_duracao_terminam_eixo_x'],
      dados_sim['cdf_duracao_terminam_eixo_y'],
      'Distribuição do tempo de duração das epidemias que terminam',
      'Duração do periodo ocupado (número de iterações)',
      'Probabilidade acumulada',
      arquivo,
      i,
      'dist_tempo_terminam',
    )

    # CDF distribuicao de filhos
    plot_cdf(
      tx_chegada,
      tx_saida,
      dados_sim['cdf_valores_eixo_x'],
      dados_sim['cdf_eixo_y'],
      'Distribuição de filhos',
      'Quantidade de filhos',
      'Probabilidade acumulada',
      arquivo,
      i,
      'dist_filhos',
    )

# Tabela de dados
# Dados da tabela:
# Media da frequencia de nascimentos
# Grau medio de saida da raiz
# Grau de saida maximo
# Altura media
# Media da duracao das epidemias que terminam
# Media do acumulado de clientes atendidos das simulacoes que terminam
data = {
  'Grau médio de\nsaída da raiz': grau_medio_saida_raiz,
  'Grau de saída\nmáximo':  grau_de_saida_maximo,
  'Altura média': altura_media,
  'Média da duração\ndas epidemias': media_duracao_epidemia,
  'Média do acumulado de\nclientes atendidos': media_acum_clientes,
}
plot_table(data)

# for v in dados_sim:
#   print(v, dados_sim[v])