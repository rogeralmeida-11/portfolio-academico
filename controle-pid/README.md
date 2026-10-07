# Controle PID digital no PIC18F1220

Controlador PID em malha fechada, implementado em C no PIC18F1220, com máquina de estados de quatro modos de operação, aritmética de ponto fixo e execução periódica temporizada por TIMER (período de 25 ms). O projeto foi simulado no Proteus 8.

📄 Relatório completo: [documento_controlador_pid_digital_pic18f1220.pdf](./documento_controlador_pid_digital_pic18f1220.pdf)

## Modos de operação

| Modo | Função |
|---|---|
| `INITIALIZATION` | Define os valores iniciais das variáveis |
| `RUN` | Executa o controle PID com cálculo de erro dinâmico |
| `MANUAL` | Controle direto da planta pelo operador |
| `SAFE` | Modo de falha, que define uma saída segura para proteger o sistema |

## Arquivos

| Arquivo | Função |
|---|---|
| `digital_pid_logic.c` | Código-fonte do firmware |
| `digital_pid_logic.hex` | Programa compilado para o PIC |
| `simulation_pic18f1220_digital_pid.pdsprj` | Circuito de simulação no Proteus |

## Ferramentas

- PIC C Compiler (CCS), pacote PCWHD, versão 5.007 (compilador PCH, para PIC18)
- Proteus 8

## Como simular

1. Abra o arquivo do Proteus no Proteus 8.
2. Dê um duplo clique no PIC18F1220 e, em **Program File**, selecione o arquivo `.hex`. `[PREENCHER: se o projeto já vem com o .hex carregado, troque este passo por essa informação]`
3. Inicie a simulação. O estado do controlador é indicado pelos LEDs do circuito.

## Resultado

A tarefa de cálculo do PID foi medida com osciloscópio em cerca de 10,55 ms, bem abaixo do período de amostragem de 25 ms.

## Demonstração

Imagens e vídeo da simulação: [site do portfólio](https://sites.google.com/view/roger-almeida/projetos#h.mh7tk3b3zk04)
