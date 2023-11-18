import sympy as sp

class Analitic:
  def __init__(self, tx_chegada, tx_saida):
    self.tx_chegada = tx_chegada
    self.tx_saida = tx_saida
    self.rho = tx_chegada / tx_saida
  
  # Caso nao deterministico
  # Transformada: G(s) = mu / mu + lambda * (1 - s)
  # A probabilidade de extincao eh o melhor valor da
  # solucao de G(s) = s
  def prob_extincao(self):
    s = sp.symbols('s')
    mu = self.tx_saida
    lambd = self.tx_chegada
    eq = mu * s - mu + lambd * s - lambd * s ** 2
    return min(sp.solve(eq, s))
  
  # Caso deterministico
  # Transformada: G(s) = e^-lambda*T(1-s)
  # Resolva a equacao: -lambd*T*(1-s) - ln(s) = 0
  def prob_extincao_det(self):
    s = sp.symbols('s')
    lambd = self.tx_chegada
    T = 1 / self.tx_saida
    eq = -lambd * T * (1 - s) - sp.log(s)
    return min(sp.solve(eq, s))

  # Se rho >= 1, E[N] = infinito
  # Se rho < 1, E[N] = 1 / (1 - rho)
  def tamanho_medio_populacao(self):
    if self.rho >= 1:
      return float('inf')
    else:
      return 1 / (1 - self.rho)
  
  # B = tempo de duracao de um periodo ocupado
  # Se rho >= 1, E[B] = infinito
  # Se rho < 1, E[B] = 1 / mu(1 - rho)
  def dur_periodo_ocupado(self):
    if self.rho >= 1:
      return float('inf')
    else:
      return 1 / (self.tx_saida * (1 - self.rho))

  def calc_metricas(self):
    print("Probabilidade de extincao: ", self.prob_extincao())
    print("Probabilidade de extincao deterministico: ", self.prob_extincao_det())
    print("Tamanho medio da populacao: ", self.tamanho_medio_populacao())
    print("Duracao do periodo ocupado: ", self.dur_periodo_ocupado())
    print('\n')

Analitic(1, 2).calc_metricas()

Analitic(2, 4).calc_metricas()

Analitic(1.05, 1).calc_metricas()

Analitic(1.10, 1).calc_metricas()
