# Hub de Projetos Acadêmicos e Portfólio

Olá, me chamo Roger Almeida. Sou graduando em Engenharia de Controle e Automação pelo Instituto Federal Fluminense (IFF), Campus Campos Centro, com previsão de formatura para o final de 2027.

Neste repositório reúno os principais projetos que desenvolvi na graduação, cada um com seu código, seus arquivos e um relatório técnico em PDF. Tenho interesse em sistemas embarcados, eletrônica, controle, sistemas supervisórios e projetos elétricos.

🌐 **Site com imagens e vídeos de demonstração:** [sites.google.com/view/roger-almeida](https://sites.google.com/view/roger-almeida)

---

## 🛠️ Projetos em Destaque

### 1. Compilador de Linguagem C feito em Python para Microcontrolador PIC18F1220

Compilador simples de C para o PIC18F1220, escrito em Python. O código em C passa pelo GCC, que gera a representação `.gimple`; um parser traduz esse arquivo para Assembly do PIC18 e um montador converte o resultado em opcodes e gera o arquivo Intel HEX. O fluxo completo foi validado com um Pisca-LED simulado no Proteus 8, com dois LEDs alternando nas saídas RB0 e RB1.

* **Tecnologias:** C, Python, GCC (GIMPLE), Assembly PIC18, Intel HEX, Proteus 8.
* **📂 Arquivos do Projeto:** [Acessar Código e Documentação](./compilador-pic18f/)
* **📄 Relatório Técnico:** [Abrir PDF do Trabalho](./compilador-pic18f/documento_compilador_c_pic18f1220.pdf)
* **📷 Demonstração:** [Ver imagens e vídeo do projeto](https://sites.google.com/view/roger-almeida/projetos#h.cnnp8pvlqpge)

### 2. Software Embarcado de Controle PID Quadrimodal para Microcontrolador PIC18F1220

Implementação de um controlador PID em malha fechada no PIC18F1220, com cálculos em ponto fixo, execução periódica temporizada por TIMER (período de 25 ms) e uma máquina de estados com 4 modos de operação. A tarefa de cálculo foi medida com osciloscópio em cerca de 10,55 ms, bem abaixo do período de amostragem.

**Modos de operação:**

* **`INITIALIZATION` (Inicialização):** define os valores iniciais das variáveis utilizadas.
* **`RUN` (Automático):** executa o controle PID com cálculo de erro dinâmico.
* **`MANUAL` (Manual):** permite o controle direto da planta pelo operador.
* **`SAFE` (Segurança):** modo de falha que define um valor de saída seguro para proteger o sistema.

**Informações do projeto:**

* **Tecnologias:** C, PIC18F1220, máquina de estados, aritmética de ponto fixo, TIMER, Proteus 8.
* **📂 Arquivos do Projeto:** [Acessar Código e Documentação](./controle-pid/)
* **📄 Relatório Técnico:** [Abrir PDF do Trabalho](./controle-pid/documento_controlador_pid_digital_pic18f1220.pdf)
* **📷 Demonstração:** [Ver imagens e vídeo do projeto](https://sites.google.com/view/roger-almeida/projetos#h.mh7tk3b3zk04)

### 3. Interface SCADA para Controle de Temperatura

Interface de supervisão (SCADA) desenvolvida no MyScada para controlar a temperatura de uma planta simulada no Node-RED (sistema de primeira ordem). A comunicação é feita via Modbus, e a interface permite acompanhar VP e VM, ajustar os parâmetros do controlador PID e alterar o estado e o modo de operação.

* **Tecnologias:** MyScada, Node-RED, Modbus.
* **📂 Arquivos do Projeto:** [Acessar Fluxos e Telas](./interface-scada/)
* **📄 Relatório Técnico:** [Abrir PDF do Trabalho](./interface-scada/documento_scada.pdf)
* **📷 Demonstração:** [Ver imagens e vídeo do projeto](https://sites.google.com/view/roger-almeida/projetos#h.jr5lr3pjvqma)

---

## 📁 Como navegar por este repositório

Cada projeto tem uma pasta com seus arquivos. Para ver os detalhes, entre na pasta correspondente ou abra o relatório em PDF pelo link na descrição do projeto.

---

**Contato:**

* LinkedIn: [Roger Almeida](https://www.linkedin.com/in/roger-almeida-gomes-46a295166)
* E-mail: [rogeralmeida650@gmail.com](mailto:rogeralmeida650@gmail.com)
