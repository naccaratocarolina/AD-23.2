# Simulação de Fila M/M/1

Este programa simula uma fila M/M/1, que é um modelo de fila com uma única servidor (M) e chegadas de clientes seguindo uma distribuição de Poisson (M). O objetivo é analisar o comportamento do sistema, incluindo o tempo médio de espera dos clientes e o tempo ocioso do servidor.

## Flags do Programa
| Flag | Definição | Default |
|------|-----------|---------|
| -a ou --arrival_rate | Taxa de chegada de clientes | 2 |
| -s ou --service_rate | Taxa de serviço do servidor | 1 |
| -m ou --max_iter | Número máximo de iterações | 50 |
| -q ou --queue_len | Tamanho da fila M/M/1 | -1 (fila infinita) |
| -i ou --idle_server | Define se o servidor pode ficar ocioso | False |
| -n ou --num_sim | Número de simulações a serem executadas | 1 |

## Como executar o programa
Para executar o programa, você pode usar o seguinte comando:
```sh
python3 mm1.py -a ARRIVAL_RATE -s SERVICE_RATE -m MAX_ITER -q QUEUE_LEN -i IDLE_SERVER -n NUM_SIM
```

### Exemplo de execução:
```sh
python mm1_simulation.py -a 2 -s 1 -m 100 -q -1 -i True -n 5
```
Neste exemplo, a simulação será executada com uma taxa de chegada de 2 clientes por unidade de tempo, uma taxa de serviço de 1 cliente por unidade de tempo, um número máximo de iterações de 100, uma fila infinita, o servidor pode ficar ocioso e serão realizadas 5 simulações consecutivas.

### Exemplo de retorno do programa:
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