# Interface SCADA para controle de temperatura

Interface de supervisão desenvolvida no mySCADA para controlar a temperatura de uma planta simulada no Node-RED. A comunicação é feita por **Modbus TCP**: o mySCADA é o cliente e o Node-RED é o servidor.

📄 Relatório completo: [documento_interface_scada.pdf](./documento_interface_scada.pdf)

## Arquivos

| Arquivo | Função |
|---|---|
| `nodered_trabalho_supervisorio.json` | Flow do Node-RED: servidor Modbus, controlador PID e planta simulada |
| `mySCADA/` | Projeto exportado do myDESIGNER (telas, layout lateral e gráfico) |
| `documento_interface_scada.pdf` | Relatório técnico |

## Ferramentas

- Node-RED 2.2.2
- myDESIGNER / mySCADA 7.0.30
- Ambiente usado: máquina virtual Lubuntu 18.04 (VirtualBox), com o mySCADA e o Node-RED na mesma VM

**Pacotes do Node-RED necessários** (instale em Menu → Gerenciar paleta):

- `node-red-contrib-modbus`
- `node-red-dashboard`
- `node-red-contrib-pid`

## Como executar

1. No Node-RED, use **Menu → Importar** e selecione `nodered_trabalho_supervisorio.json`. Clique em **Deploy**.
2. No myDESIGNER, abra o projeto da pasta `mySCADA/` `[PREENCHER: como importar o projeto exportado]`.
3. Configure a conexão Modbus TCP do mySCADA com os dados abaixo e inicie a visualização.

| Parâmetro | Valor |
|---|---|
| Protocolo | Modbus TCP |
| Endereço | `127.0.0.1` (mySCADA e Node-RED na mesma máquina) |
| Porta | `10502` |
| Unit ID | `1` |

## Registradores (holding registers, endereços a partir de 0)

| Endereço | Variável | Sentido |
|---|---|---|
| HR0 | Liga/Desliga do PID | SCADA → Node-RED |
| HR1 | Modo (1 = manual, 0 = automático) | SCADA → Node-RED |
| HR2 | Setpoint | SCADA → Node-RED |
| HR3 | Banda proporcional | SCADA → Node-RED |
| HR4 | Tempo integrativo | SCADA → Node-RED |
| HR5 | Tempo derivativo | SCADA → Node-RED |
| HR6 | Temperatura do fluido (VP) | Node-RED → SCADA |
| HR7 | Abertura da válvula (VM) | Node-RED → SCADA |

## Modos de operação

- **Manual:** o PID usa o liga/desliga, o setpoint e os parâmetros ajustados no SCADA.
- **Automático:** o PID usa valores predefinidos pelo próprio flow (setpoint 80 e banda proporcional, Ti e Td iguais a 0, o que faz o controlador atuar como liga/desliga). O setpoint e os parâmetros do SCADA são ignorados.

O botão ON/OFF só tem efeito no modo manual. Mais detalhes na seção 4.2 do relatório.

## Demonstração

Imagens e vídeo da interface em funcionamento: [site do portfólio](https://sites.google.com/view/roger-almeida/projetos#h.jr5lr3pjvqma)
