# Compilador de C para PIC18F1220

Compilador simples, escrito em Python, que traduz um código em C para Assembly do PIC18F1220 e gera um arquivo Intel HEX para gravar no chip. O fluxo foi validado com um Pisca-LED simulado no Proteus 8.

> O processo **não é totalmente automatizado**: a geração do `.gimple` é feita à parte, com um comando do GCC no terminal. A partir do `.gimple`, o `parser.py` executa o resto em sequência.

📄 Relatório completo: [documento_compilador_c_pic18f1220.pdf](./documento_compilador_c_pic18f1220.pdf)

## Arquivos

| Arquivo | Função |
|---|---|
| `LED_BlinkC.c` | Exemplo em C usado no teste (Pisca-LED) |
| `parser.py` | Programa principal: lê o `.gimple` e gera, em sequência, o `.asm`, a lista de opcodes e o `.hex` |
| `asm_lib.py` | Biblioteca de geração de Assembly (mapeamento de variáveis e instruções) |
| `hex_lib.py` | Montador: converte as instruções em opcodes e escreve o Intel HEX |
| `simulation_circuit.pdsprj` | Arquivo do circuito de simulação no Proteus |

## Ferramentas

- Python `3.13.2`
- GCC `15.1.0`
- VS Code
- Proteus 8 (simulação)

## Como executar

1. **Gerar o GIMPLE** a partir do código em C (etapa manual, no terminal):

   ```
   gcc -c -O0 -fdump-tree-gimple LED_BlinkC.c
   ```

2. **Rodar o parser** sobre o `.gimple`:

   ```
   python parser.py
   ```

   Com o `.gimple` disponível, esse único passo gera o `.asm`, depois a lista de opcodes e, a partir dela, o `.hex`.

3. **Simular:** no Proteus 8, abra o circuito com o PIC18F1220 e LEDs em RB0 e RB1, carregue o `.hex` no microcontrolador e inicie a simulação.

## Limitações

- O compilador foi testado apenas com o exemplo do Pisca-LED, então cobre somente o subconjunto do GIMPLE necessário para ele.
- A geração do `.gimple` com o GCC não está integrada ao `parser.py` e precisa ser feita manualmente antes.

## Demonstração

Imagens e vídeo da simulação: [site do portfólio](https://sites.google.com/view/roger-almeida/projetos#h.cnnp8pvlqpge)
