import random
from public.common import *

class Gambler:
  def __init__(self, initial_capital, bet_amount, win_prob):
    self.capital = initial_capital # Capital inicial
    self.bet_amount = bet_amount # Valor da aposta
    self.win_prob = win_prob # Probabilidade de ganhar a aposta
    self.loss_prob = 1 - win_prob # Probabilidade de perder a aposta
    self.capital_log = [(0, self.capital)] # Log de capital
    self.rounds = 0 # Contador de rodadas

  def bet(self):
    # Sorteia se o jogador ganhou ou perdeu a aposta
    bet = random.choices([True, False], weights=[self.win_prob, self.loss_prob])[0]

    # Atualiza o capital do jogador
    if bet:
      self.capital += self.bet_amount
    else:
      self.capital -= self.bet_amount

    # Atualiza contador de rodadas e log de capital
    self.rounds += 1
    self.capital_log.append((self.rounds, self.capital))

    gambler_log(self, bet)

def run(gambler, goal):
  # Simula apostas até que o jogador fique sem dinheiro ou atinja o objetivo
  while gambler.capital > 0 and gambler.capital < goal:
    gambler.bet()

if __name__ == "__main__":
  # Parsear flags
  args = gambler_parse_flags()
  initial_capital = args.initial_capital
  bet_amount = args.bet_amount
  win_prob = args.win_prob
  goal = args.goal
  num_sim = args.num_sim

  # Imprime estado inicial
  print(f'Capital inicial: {initial_capital}')
  print(f'Objetivo: {goal}')
  print(f'Valor da aposta: {bet_amount}\n')

  # Executa simulação
  for _ in range(num_sim):
    sim_log(f'Simulação {(_+1):02d}')
    gambler = Gambler(initial_capital, bet_amount, win_prob)
    run(gambler, goal)
    gambler_result(gambler, goal)
