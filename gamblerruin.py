import random

# Cores para print
LOSS_COLOR = '\033[31m' # Vermelho
WIN_COLOR = '\033[32m' # Verde
RESET_COLOR = '\033[0m'

class Gambler:
  def __init__(self, initial_capital, bet_amount, win_prob):
    self.capital = initial_capital
    self.bet_amount = bet_amount
    self.win_prob = win_prob
    self.loss_prob = 1 - win_prob
    self.capital_log = [(0, self.capital)]
    self.rounds = 0

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
      print(f'{WIN_COLOR}Rodada {self.rounds} | Ganhou {self.bet_amount} | Balanço: {self.capital}{RESET_COLOR}')
    else:
      print(f'{LOSS_COLOR}Rodada {self.rounds} | Perdeu {self.bet_amount} | Balanço: {self.capital}{RESET_COLOR}')

def run(gambler, goal):
  # Simula apostas até que o jogador fique sem dinheiro ou atinja o objetivo
  while gambler.capital > 0 and gambler.capital < goal:
    gambler.bet()

if __name__ == "__main__":
  initial_capital = 10
  bet_amount = 1
  win_prob = 0.5
  goal = 12

  print(f'Capital inicial: {initial_capital}')
  print(f'Objetivo: {goal}')
  print(f'Valor da aposta: {bet_amount}\n')

  gambler = Gambler(initial_capital, bet_amount, win_prob)
  run(gambler, goal)

  if gambler.capital == 0:
    print(f'\nO jogador faliu em {gambler.rounds} rodadas')
  elif gambler.capital == goal:
    print(f'\nO jogador atingiu o objetivo em {gambler.rounds} rodadas')
