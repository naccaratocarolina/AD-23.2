import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import glob
import os
from mm1_epidemy import mm1_epidemy

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

def plot_cdf(tx_chegada, tx_saida, dados_sim, arquivo):
  # Extrai caso do nome do arquivo
  caso = arquivo.split('.')[1]

  # Dados da CDF
  cdf_valores_eixo_x = dados_sim['cdf_valores_eixo_x']
  cdf_eixo_y = dados_sim['cdf_eixo_y']

  # Gera grafico da CDF
  plt.figure(figsize=(8, 6))
  plt.title(f'Distribuição de filhos {caso}: λ={tx_chegada}, μ={tx_saida}')

  # Interpolação linear
  f = interp1d(cdf_valores_eixo_x, cdf_eixo_y, kind='linear')
  eixo_x = np.linspace(min(cdf_valores_eixo_x), max(cdf_valores_eixo_x), num=1000, endpoint=True)
  eixo_y = np.array(f(eixo_x))

  plt.plot(eixo_x, eixo_y, label='CDF contínua')
  plt.step(cdf_valores_eixo_x, cdf_eixo_y, label='CDF discreta', where='post', linestyle='--', color='red', alpha=0.5)
  plt.xlabel('Quantidade de filhos')
  plt.ylabel('Probabilidade acumulada')
  plt.legend()
  plt.savefig(f'graficos/{arquivo}.png')
  plt.show()

# Abre todos os arquivos na pasta dados
for arquivo in glob.glob("dados/*.json"):
  # Abre o arquivo JSON
  with open(arquivo) as f:
    dados_json = json.load(f)
    tx_chegada = dados_json['tx_chegada']
    tx_saida = dados_json['tx_saida']
    dados_sim = dados_json['sims'][-1]

    plot_cdf(tx_chegada, tx_saida, dados_sim, os.path.basename(arquivo))

# for v in dados_sim:
#   print(v, dados_sim[v])