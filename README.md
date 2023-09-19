## Simulação de Fila M/M/1

Este programa simula uma fila M/M/1, que é um modelo de fila com uma única servidor (M) e chegadas de clientes seguindo uma distribuição de Poisson (M). O objetivo é analisar o comportamento do sistema, incluindo o tempo médio de espera dos clientes e o tempo ocioso do servidor.

### Flags do Programa
| Flag | Definição | Default |
|------|-----------|---------|
| -a ou --arrival_rate | Taxa de chegada de clientes | 2 |
| -s ou --service_rate | Taxa de serviço do servidor | 1 |
| -m ou --max_iter | Número máximo de iterações | 50 |
| -q ou --queue_len | Tamanho da fila M/M/1 | -1 (fila infinita) |
| -i ou --idle_server | Define se o servidor pode ficar ocioso | False |
| -n ou --num_sim | Número de simulações a serem executadas | 1 |

### Como executar o programa
Para executar o programa, você pode usar o seguinte comando:
```sh
python3 mm1.py -a ARRIVAL_RATE -s SERVICE_RATE -m MAX_ITER -q QUEUE_LEN -i IDLE_SERVER -n NUM_SIM
```

#### Exemplo de execução:
```sh
python mm1_simulation.py -a 2 -s 1 -m 100 -q -1 -i True -n 5
```
Neste exemplo, a simulação será executada com uma taxa de chegada de 2 clientes por unidade de tempo, uma taxa de serviço de 1 cliente por unidade de tempo, um número máximo de iterações de 100, uma fila infinita, o servidor pode ficar ocioso e serão realizadas 5 simulações consecutivas.

#### Exemplo de retorno do programa:
```sh
Simulação 01
0.00: Cliente chega N = 1
0.38: Cliente é atendido Tempo de espera: 0.38
0.38: Servidor ocioso N = 0
0.53: Cliente chega N = 1
1.04: Cliente chega N = 2
1.32: Cliente chega N = 3
1.63: Servidor volta a atender clientes após 1.25
1.63: Cliente é atendido Tempo de espera: 1.09
1.79: Cliente chega N = 3
2.57: Cliente chega N = 4
2.60: Cliente chega N = 5
3.05: Cliente chega N = 6
3.12: Cliente chega N = 7

Estatísticas:
Número de clientes atendidos: 2
Tempo médio de espera: 0.74
Servidor ficou oscioso 1 vezes com tempo médio de 1.25
Tempo final da simulação: 3.12
```

## Gambler's Ruin

### Flags do Programa
| Flag                | Definição                          | Default |
|---------------------|------------------------------------|---------|
| --initial-capital   | Capital inicial do jogador         | 1       |
| --bet-amount        | Valor da aposta                    | 1       |
| --win-prob          | Probabilidade de ganhar a aposta   | 0.5     |
| --goal              | Objetivo do jogador                 | 5       |
| --max-iter          | Número máximo de iterações          | 3       |

### Como executar o programa
Para executar o programa, você pode usar o seguinte comando:
```sh
python3 gamblerruin.py --initial-capital INITIAL_CAPITAL --bet-amount BET_AMOUNT --win-prob WIN_PROB --goal GOAL --max-iter MAX_ITER
```

#### Exemplo de execução:
```sh
python3 gamblerruin.py --initial-capital 1 --bet-amount 1 --win-prob 0.4 --goal 5 --max-iter 5
```
Neste exemplo, a simulação será executada com um capital inicial de 1, um valor de aposta de 1, uma probabilidade de ganhar a aposta de 40%, um objetivo de 5 e um número máximo de iterações de 5.

#### Exemplo de retorno do programa:
```sh
Capital inicial: 1
Objetivo: 5
Valor da aposta: 1

Simulação 01
Rodada 1 | Perdeu 1 | Saldo: 0

O jogador faliu em 1 rodadas

Simulação 02
Rodada 1 | Ganhou 1 | Saldo: 2
Rodada 2 | Perdeu 1 | Saldo: 1
Rodada 3 | Perdeu 1 | Saldo: 0

O jogador faliu em 3 rodadas

Simulação 03
Rodada 1 | Ganhou 1 | Saldo: 2
Rodada 2 | Perdeu 1 | Saldo: 1
Rodada 3 | Ganhou 1 | Saldo: 2
Rodada 4 | Perdeu 1 | Saldo: 1
Rodada 5 | Perdeu 1 | Saldo: 0

O jogador faliu em 5 rodadas

Simulação 04
Rodada 1 | Perdeu 1 | Saldo: 0

O jogador faliu em 1 rodadas

Simulação 05
Rodada 1 | Perdeu 1 | Saldo: 0

O jogador faliu em 1 rodadas
```