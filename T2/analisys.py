import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os

def plot_cdf(dados_json):
  # Gera grafico da CDF acumulada
  plt.figure(figsize=(8, 6))
  plt.title('CDF acumulada')

  # Interpolação linear
  cdf_valores_eixo_x = dados_sim['cdf_valores_eixo_x']
  cdf_acumulada_eixo_y = dados_sim['cdf_acumulada_eixo_y']

  f = interp1d(cdf_valores_eixo_x, cdf_acumulada_eixo_y, kind='linear')
  eixo_x = np.linspace(min(cdf_valores_eixo_x), max(cdf_valores_eixo_x), num=1000, endpoint=True)
  eixo_y = np.array(f(eixo_x))

  plt.plot(eixo_x, eixo_y, label='CDF contínua')
  plt.step(cdf_valores_eixo_x, cdf_acumulada_eixo_y, label='CDF discreta', where='post', linestyle='--', color='red', alpha=0.5)
  plt.xlabel('Quantidade de filhos')
  plt.ylabel('Probabilidade acumulada')
  plt.legend()
  plt.savefig(f'graficos/{arquivo}.png')
  plt.show()

# Abre todos os arquivos na pasta dados
caminho = '/dados'
for arquivo in os.listdir(caminho):
  caminho_completo = os.path.join(caminho, arquivo)
  if os.path.isfile(caminho_completo):
    with open(f'{arquivo}', 'r') as arquivo_json:
      # Carregar o conteúdo do arquivo JSON
      dados_json = json.load(arquivo_json)

      dados_sim = dados_json['sims'][-1]

      plot_cdf(dados_json)

# for v in dados_sim:
#   print(v, dados_sim[v])