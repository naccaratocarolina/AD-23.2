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

# # Roda as simulacoes
# epidemia_caso1.run_mm1_epid()
# epidemia_caso2.run_mm1_epid()
# epidemia_caso3.run_mm1_epid()
# epidemia_caso4.run_mm1_epid()

def plot_cdf(tx_chegada, tx_saida, eixo_x, eixo_y, title, xlabel, ylabel, caso, arquivo):
  nome_arquivo = arquivo.replace('dados/', '').replace('.json', '')

  if (len(eixo_x) <= 1):
    print(f'Não há dados suficientes para gerar o gráfico de {arquivo}!')
    return

  # Gera grafico da CDF
  plt.figure(figsize=(8, 6))
  plt.title(f'{title} (Caso {caso}): λ={tx_chegada}, μ={tx_saida}')

  # Interpolação linear
  f = interp1d(eixo_x, eixo_y, kind='linear', fill_value='extrapolate')
  eixo_x_interp = np.linspace(min(eixo_x), max(eixo_x), num=len(eixo_x), endpoint=True)
  eixo_y_interp = np.array(f(eixo_x_interp))

  # o plot tem que ter len(eixo_x) pontos para que a CDF seja corretamente plotada
  # por isso, o eixo x interpolado tem que ter len(eixo_x) pontos

  plt.plot(eixo_x_interp, eixo_y_interp, label='CDF contínua')
  plt.step(eixo_x, eixo_y, label='CDF discreta', where='post', linestyle='--', color='red', alpha=0.5)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ticklabel_format(style='plain', axis='x')
  plt.legend()
  plt.savefig(f'graficos/{nome_arquivo}')
  plt.close()
  print(f'Gráfico {nome_arquivo} gerado com sucesso!')
  # plt.show()

# Estrutura de data:
# { title1: [value1], title2: [value2], ... }
def plot_table(df, title='Tabela de dados'):
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

  # set the title
  plt.title(title, fontsize=20)
  
  plt.savefig('graficos/tabela.png')
  plt.close()
  print('Tabela gerada com sucesso!')

# Dados para a tabela
grau_medio_saida_raiz = []
grau_de_saida_maximo = []
altura_media = []
altura_media_nos = []
media_duracao_periodo_ocupado = []
media_clientes_atendidos = []

# Cabeçalho da tabela
header = [
  'Caso',
  'Grau médio de\nsaída da raiz',
  'Grau de saída\nmáximo',
  'Altura média',
  'Altura média dos nós',
  'Média da duração\ndas epidemias',
  'Média do acumulado de\nclientes atendidos',
]

df = pd.DataFrame(columns=header)

def format_float(value):
  return f'{value:.2f}'

# Abre todos os arquivos na pasta dados
for i, arquivo in enumerate(glob.glob("dados/*.json")):
  caso = arquivo.split('.')[1][-1]
  # Abre o arquivo JSON
  with open(arquivo) as f:
    dados_json = json.load(f)
    tx_chegada = dados_json['tx_chegada']
    tx_saida = dados_json['tx_saida']
    
    for type in ['terminam', 'todas']:
      terminam = 'Epidemias que terminam' if type == 'terminam' else 'Todas as epidemias'
      dados_sim = dados_json[type]

      # constroi plot da CDF a partir do array de distribuicao de grau de saida
      # eixo x é um array com os indices do array de distribuicao de grau de saida
      eixo_x = np.arange(len(dados_sim['dist_grau_saida']), dtype=int)
      # eixo y é um array com a soma acumulada dos valores do array de distribuicao de grau de saida
      eixo_y = dados_sim['dist_grau_saida']
      eixo_y = np.cumsum(eixo_y)

      # CDF distribuicao de filhos
      plot_cdf(
        tx_chegada,
        tx_saida,
        eixo_x,
        eixo_y,
        f'CDF da quantidade de filhos ({terminam})',
        'Quantidade de filhos',
        'Probabilidade acumulada',
        caso,
        arquivo.replace('.json', f'.cdf_filhos.{type}.png')
      )

    # Constuir a tabela de dados
    dt_terminam = dados_json['terminam']
    dt_todas = dados_json['todas']

    # Dados para a tabela
    linha = [
      f"Caso {caso} (terminam | todas)",
      f"{format_float(dt_terminam['grau_medio_saida_raiz'])} | {format_float(dt_todas['grau_medio_saida_raiz'])}",
      f"{format_float(dt_terminam['grau_de_saida_maximo'])} | {format_float(dt_todas['grau_de_saida_maximo'])}",
      f"{format_float(dt_terminam['altura_media'])} | {format_float(dt_todas['altura_media'])}",
      f"{format_float(dt_terminam['altura_media_nos'])} | {format_float(dt_todas['altura_media_nos'])}",
      f"{format_float(dt_terminam['media_duracao_periodo_ocupado'])} | {format_float(dt_todas['media_duracao_periodo_ocupado'])}",
      f"{format_float(dt_terminam['media_clientes_atendidos'])} | {format_float(dt_todas['media_clientes_atendidos'])}"
    ]

    # adiciona linha na df
    df.loc[i] = linha

  plot_table(df, title=f'Tabela de dados')

# for v in dados_sim:
#   print(v, dados_sim[v])