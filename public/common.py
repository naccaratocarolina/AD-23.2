import argparse

# Cores para print
SIM_COLOR = '\033[30m' # Preto
SIM_BACKGROUND_COLOR = '\033[47m' # Fundo branco
RESET_COLOR = '\033[0m' # Resetar cor

# MM1
ARRIVAL_COLOR = '\033[33m' # Amarelo
DEPARTURE_COLOR = '\033[34m' # Azul
IDLE_COLOR = '\033[35m' # Magenta

# Gambler
LOSS_COLOR = '\033[31m' # Vermelho
WIN_COLOR = '\033[32m' # Verde

# Log de simulação
def sim_log(msg):
  print(f'{SIM_COLOR}{SIM_BACKGROUND_COLOR}{msg}{RESET_COLOR}')

# Log de MM1
def mm1_log(msg, clock, type):
  if type == 'arrival':
    print(f'{ARRIVAL_COLOR}{clock:.2f}: {msg}{RESET_COLOR}')
  elif type == 'departure':
    print(f'{DEPARTURE_COLOR}{clock:.2f}: {msg}{RESET_COLOR}')
  elif type == 'idle':
    print(f'{IDLE_COLOR}{clock:.2f}: {msg}{RESET_COLOR}')

# Função para parsear flags de MM1
def mm1_parse_flags():
  parser = argparse.ArgumentParser(description='Simulação de fila M/M/1')
  parser.add_argument('-a', '--arrival_rate', type=float, default=2, help='Taxa de chegada de clientes')
  parser.add_argument('-s', '--service_rate', type=float, default=1, help='Taxa de serviço do servidor')
  parser.add_argument('-m', '--max_iter', type=int, default=-1, help='Número máximo de iterações')
  parser.add_argument('-q', '--queue_len', type=int, default=-1, help='Tamanho da fila M/M/1')
  parser.add_argument('-i', '--idle_server', type=bool, default=False, help='Servidor pode ficar ocioso')
  parser.add_argument('-n', '--num_sim', type=int, default=1, help='Número de simulações')
  
  return parser.parse_args()

# Log de Gambler
def gambler_log(gambler, won_round):
    if won_round:
      print(f'Rodada {gambler.rounds} | {WIN_COLOR}Ganhou {gambler.bet_amount}{RESET_COLOR} | Saldo: {gambler.capital}')
    else:
      print(f'Rodada {gambler.rounds} | {LOSS_COLOR}Perdeu {gambler.bet_amount}{RESET_COLOR} | Saldo: {gambler.capital}')

# Log de resultado de Gambler
def gambler_result(gambler, goal):
  if gambler.capital == 0:
      print(f'\nO jogador {LOSS_COLOR}faliu{RESET_COLOR} em {gambler.rounds} rodadas\n')
  elif gambler.capital == goal:
    print(f'\nO jogador {WIN_COLOR}ganhou{RESET_COLOR} em {gambler.rounds} rodadas\n')

# Função para parsear flags de Gambler
def gambler_parse_flags():
  parser = argparse.ArgumentParser(description='Simulação de apostas')
  parser.add_argument('-c', '--initial-capital', type=int, default=1, help='Capital inicial do jogador')
  parser.add_argument('-b','--bet-amount', type=int, default=1, help='Valor da aposta')
  parser.add_argument('-w','--win-prob', type=float, default=0.5, help='Probabilidade de ganhar a aposta')
  parser.add_argument('-g','--goal', type=int, default=5, help='Objetivo do jogador')
  parser.add_argument('-n','--num_sim', type=int, default=1, help='Número máximo de iterações')
  return parser.parse_args()