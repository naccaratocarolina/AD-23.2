import simpy
import random

# Cores para print
LOSS_COLOR = '\033[31m' # Vermelho
WIN_COLOR = '\033[32m' # Verde
RESET_COLOR = '\033[0m'

class Gambler:
  def __init__(self, env, initial_capital, bet_amount, win_prob):
    self.env = env # Ambiente de simulação
    self.capital = initial_capital # Balanço inicial
    self.bet_amount = bet_amount # Valor da aposta
    self.win_prob = win_prob # Probabilidade de ganhar
    self.loss_prob = (1 - win_prob) # Probabilidade de perder
    self.capital_log = [(0, self.capital)] # Lista de balanços
    self.rounds = 0 # Número de rodadas
  
  # Handler para evento de aposta
  def bet(self):
    # Sortear resultado da aposta
    bet = random.choices([True, False], weights=[self.win_prob, self.loss_prob])[0]
    
    # Atualizar balanço
    if bet:
      self.capital += self.bet_amount
    else:
      self.capital -= self.bet_amount

    # Avança o tempo em uma unidade (uma rodada)
    self.rounds += 1
    yield self.env.timeout(1)

    # Adiciona balanço atual à lista de balanços
    self.capital_log.append((self.rounds, self.capital))

    gambler.gambler_log(bet)
  
  def gambler_log(self, won_round):
    if won_round:
      print(f'{WIN_COLOR}Rodada {self.rounds} | Ganhou {self.bet_amount} | Balanço: {self.capital}{RESET_COLOR}')
    else:
      print(f'{LOSS_COLOR}Rodada {self.rounds} | Perdeu {self.bet_amount} | Balanço: {self.capital}{RESET_COLOR}')

def run(env, gambler, goal):
  while gambler.capital > 0 and gambler.capital < goal:
    yield env.process(gambler.bet())

if __name__ == "__main__":
  initial_capital = 1 # Balanço inicial
  bet_amount = 1 # Valor da aposta
  win_prob = 0.51 # Probabilidade de ganhar
  goal = 4 # Objetivo

  # Imprime quantidade inicial, objetivo e valor da aposta
  print(f'Capital inicial: {initial_capital}')
  print(f'Objetivo: {goal}')
  print(f'Valor da aposta: {bet_amount}\n')

  env = simpy.Environment() # Cria ambiente de simulação
  gambler = Gambler(env, initial_capital, bet_amount, win_prob) # Cria jogador
  env.process(run(env, gambler, goal)) # Adiciona jogador ao ambiente de simulação
  env.run() # Roda a simulação

  # Imprime se houve ruina ou não
  if gambler.capital == 0:
    print(f'\nO jogador faliu')
  elif gambler.capital == goal:
    print(f'\nO jogador atingiu o objetivo')