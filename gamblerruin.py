import random
import argparse

# Cores para print
SIM_COLOR = '\033[30m' # Preto
SIM_BACKGROUND_COLOR = '\033[47m' # Fundo branco
LOSS_COLOR = '\033[31m' # Vermelho
WIN_COLOR = '\033[32m' # Verde
RESET_COLOR = '\033[0m'

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

    self.gambler_log(bet)

  def gambler_log(self, won_round):
    if won_round:
      print(f'Rodada {self.rounds} | {WIN_COLOR}Ganhou {self.bet_amount}{RESET_COLOR} | Saldo: {self.capital}')
    else:
      print(f'Rodada {self.rounds} | {LOSS_COLOR}Perdeu {self.bet_amount}{RESET_COLOR} | Saldo: {self.capital}')

def run(gambler, goal):
  # Simula apostas até que o jogador fique sem dinheiro ou atinja o objetivo
  while gambler.capital > 0 and gambler.capital < goal:
    gambler.bet()

def parse_args():
  parser = argparse.ArgumentParser(description='Simulação de apostas')
  parser.add_argument('-c', '--initial-capital', type=int, default=1, help='Capital inicial do jogador')
  parser.add_argument('-b','--bet-amount', type=int, default=1, help='Valor da aposta')
  parser.add_argument('-w','--win-prob', type=float, default=0.5, help='Probabilidade de ganhar a aposta')
  parser.add_argument('-g','--goal', type=int, default=5, help='Objetivo do jogador')
  parser.add_argument('-n','--num_sim', type=int, default=1, help='Número máximo de iterações')
  return parser.parse_args()

if __name__ == "__main__":
  # Parsear flags
  args = parse_args()
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
    print(f'{SIM_COLOR}{SIM_BACKGROUND_COLOR}Simulação {(_+1):02d}{RESET_COLOR}')
    gambler = Gambler(initial_capital, bet_amount, win_prob)
    run(gambler, goal)

    if gambler.capital == 0:
      print(f'\nO jogador {LOSS_COLOR}faliu{RESET_COLOR} em {gambler.rounds} rodadas\n')
    elif gambler.capital == goal:
      print(f'\nO jogador {WIN_COLOR}ganhou{RESET_COLOR} em {gambler.rounds} rodadas\n')
