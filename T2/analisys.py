import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import glob
from mm1_epidemy import mm1_epidemy
import pandas as pd
from matplotlib.font_manager import FontProperties

def gera_info_text(ehInfinita, ehDeterministica, termina):
  info = ''
  if (ehInfinita):
    info = 'Epidemia infinita\n'
  else:
    info = 'Epidemia finita\n'
  
  if (termina):
    info += 'Epidemias que terminam'
  else:
    info += 'Todas as epidemias'
  
  if (ehDeterministica):
    info += '\nTempo de serviço determinístico'

  return info

def plot_cdf(
    tx_chegada,
    tx_saida,
    eixo_x, # Lista com os valores do eixo x
    eixo_y, # Lista com os valores do eixo y
    title,
    xlabel,
    ylabel,
    caso,
    nome_arquivo,
    ehInfinita,
    ehDeterministica,
    termina,
  ):
  if (len(eixo_x) <= 1):
    print(f'Não há dados suficientes para gerar o gráfico de {nome_arquivo}!')
    return

  # Gera grafico da CDF
  plt.figure(figsize=(8, 6))
  plt.title(f'{title} (Caso {caso}): λ={tx_chegada}, μ={tx_saida}')

  # Interpolação linear
  f = interp1d(eixo_x, eixo_y, kind='linear', fill_value='extrapolate')
  eixo_x_interp = np.linspace(min(eixo_x), max(eixo_x), num=len(eixo_x), endpoint=True)
  eixo_y_interp = np.array(f(eixo_x_interp))

  # Informacoes adicionais
  info = gera_info_text(ehInfinita, ehDeterministica, termina)

  # o plot tem que ter len(eixo_x) pontos para que a CDF seja corretamente plotada
  # por isso, o eixo x interpolado tem que ter len(eixo_x) pontos

  plt.plot(eixo_x_interp, eixo_y_interp, label='CDF contínua')
  plt.step(eixo_x, eixo_y, label='CDF discreta', where='post', linestyle='--', color='red', alpha=0.5)
  plt.annotate(info, xy=(0.5, 0.05), xycoords='axes fraction', ha='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ticklabel_format(style='plain', axis='x')
  plt.legend()
  plt.savefig(f'graficos/{nome_arquivo}')
  plt.close()
  print(f'Gráfico {nome_arquivo} gerado com sucesso!')

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

def plot_graph(
  tx_chegada,
  tx_saida,
  eixo_x, # Lista com os valores do eixo x
  eixo_y, # Lista com os valores do eixo y
  title,
  xlabel,
  ylabel,
  caso,
  nome_arquivo,
  ehInfinita,
  ehDeterministica,
  termina,
):
  if (len(eixo_x) <= 1):
    print(f'Não há dados suficientes para gerar o gráfico de {nome_arquivo}!')
    return

  # Calcula o intervalo de confiança de 95%
  media = np.mean(eixo_y)
  std_dev = np.std(eixo_y)
  n = len(eixo_y)
  z_score = 1.96 # Valor crítico para intervalo de confiança de 95%
  margem_erro = z_score * (std_dev / np.sqrt(n))

  lim_sup = eixo_y + margem_erro
  lim_inf = eixo_y - margem_erro

  # Informacoes adicionais
  info = gera_info_text(ehInfinita, ehDeterministica, termina)

  # Gera gráfico
  plt.figure(figsize=(9, 7))
  plt.title(f'{title} (Caso {caso}): λ={tx_chegada}, μ={tx_saida}')
  plt.plot(eixo_x, eixo_y, label=title, marker='o')
  plt.fill_between(eixo_x, lim_inf, lim_sup, alpha=0.2, label='Intervalo de confiança de 95%')
  plt.annotate(info, xy=(0.5, 0.05), xycoords='axes fraction', ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ticklabel_format(style='plain', axis='x')
  plt.legend()
  plt.savefig(f'graficos/{nome_arquivo}')
  plt.close()
  print(f'Gráfico {nome_arquivo} gerado com sucesso!')

def format_float(value):
  return f'{value:.2f}'

def run_analisys():
  # Cabeçalho da tabela
  header = [
    'Caso (terminam | todas)',
    'Grau médio de\nsaída da raiz',
    'Grau de saída\nmáximo',
    'Altura média',
    'Altura média dos nós',
    'Média da duração\ndas epidemias',
    'Média do acumulado de\nclientes atendidos',
  ]

  # Cria dataframe vazio com o cabeçalho
  df = pd.DataFrame(columns=header)

  # Abre todos os arquivos na pasta dados
  for i, arquivo in enumerate(glob.glob("dados/*.json")):
    caso = arquivo.split('.')[1][-1]
    # Abre o arquivo JSON
    with open(arquivo) as f:
      dados_json = json.load(f)
      tx_chegada = dados_json['tx_chegada']
      tx_saida = dados_json['tx_saida']
      ehInfinita = True if ('infinita' in arquivo) else False
      ehDeterministica = True if ('deterministico' in arquivo) else False
      
      for type in ['terminam', 'todas']:
        termina = True if (type == 'terminam') else False
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
          'CDF da quantidade de filhos',
          'Quantidade de filhos',
          'Probabilidade acumulada',
          caso,
          f'{i}_caso_{caso}.cdf_filhos.{type}.png',
          ehInfinita,
          ehDeterministica,
          termina,
        )

        # Imprime grafico da media do numero de infectados por geracao
        eixo_y = dados_sim['media_infectados_por_geracao']
        eixo_x = np.arange(len(eixo_y)).astype(int)
        plot_graph(
          tx_chegada,
          tx_saida,
          eixo_x,
          eixo_y,
          'Média do número de infectados por geração',
          'Geração',
          'Número de infectados',
          caso,
          f'{i}_caso_{caso}.media_infectados.{type}.png',
          ehInfinita,
          ehDeterministica,
          termina,
        )

      # Constuir a tabela de dados
      dt_terminam = dados_json['terminam']
      dt_todas = dados_json['todas']

      # Dados para a tabela
      linha = [
        f"Caso {caso}",
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
