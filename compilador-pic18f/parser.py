import re
import os
import asm_lib
import hex_lib

# ==================================================================================================================================================================
#|||PARSING DE CODIGO C PARA PIC18F1220|||
# ==================================================================================================================================================================
#|||GERAÇAO DO ASSEMBLY|||
#Dicionario das variaveis que serao necessarias armazenar
variaveis_codigo = {'ponteiro':{'nome':None,'tipo':None,'endereço':0},'label':{'para ignorar':None}}

#Variaveis de estado para rastreio de sequencia do codigo de incremento e condicional
estado_sequencia_inc = 0
estado_sequencia_cond = 0
estado_sequencia_at = 0

# Nome do arquivo GIMPLE que sera utilizado
gimple_filename = "LED_BlinkC.c.007t.gimple"

LED_Blink, _ = os.path.splitext(gimple_filename)
asm_filename = LED_Blink + ".asm"

print(f"\n--- Iniciando parsing asm do arquivo: {gimple_filename} ---")

#Abrindo arquivo de entrada .gimple e gerando um arquivo de saida .asm
try:
    # 'with open' abre o arquivo e garante que ele sera fechado no final
    with open(gimple_filename, 'r', encoding='utf-8') as infile, \
             open(asm_filename, 'w', encoding='utf-8') as outfile:
        # Loop que le o arquivo linha por linha
        for line_number, line in enumerate(infile, 1):
            # line.strip() remove espacos em branco e quebras de linha inuteis
            clean_line = line.strip()

            # Ignora linhas em branco
            if not clean_line:
                continue

            # =========================================================
            # //LOGICA DO PARSER//
                        
            if line_number == 1:
            #|CONFIGURAÇOES DO PIC18F1220|
                asm_lib.config_pic(outfile)

            #|INICIO DO PROGRAMA|
                outfile.write('        ORG 0x00\n\n')

            #|NECESSIDADE OU NAO DE PULAR PARA MAIN() NO INICIO DO CODIGO|
                if (clean_line == 'main()'):
                    pass
                else:
                    outfile.write('        GOTO MAIN\n')

            #|LABELS DE FUNÇOES|
            padrao_lf = re.compile(r'(?:void\s)?(\w+)(?:_\w+)?\s*\(\s*\)$')
            correspondencia_lf = padrao_lf.search(clean_line)

            if correspondencia_lf:
                label_function = correspondencia_lf.group(1)
                lb_function_upper = label_function.upper()
                asm_lib.label_de_funcoes(lb_function_upper,outfile)

            #|LABEL SIMPLES|
            padrao_l = re.compile(rf'<(?!{variaveis_codigo['label']['para ignorar']})(\w+)\.(\d+)>:')
            correspondencia_l = padrao_l.fullmatch(clean_line)

            if correspondencia_l:
                lb_letra = correspondencia_l.group(1)
                lb_numero = correspondencia_l.group(2)
                asm_lib.label_simples(lb_letra,lb_numero,outfile)
            
            #|ATRIBUIÇOES SIMPLES|
            padrao_at_linha1 = re.compile(rf'((?!{variaveis_codigo['ponteiro']['nome']})\w+)\s*=\s*((?!{variaveis_codigo['ponteiro']['nome']})\w+)\s*;')
            padrao_at_linha2 = re.compile(rf'\*((?!{variaveis_codigo['ponteiro']['nome']})\w+)\s*=\s*(\d+)\s*;')

            if estado_sequencia_at == 0:
                correspondencia_at_1 = padrao_at_linha1.search(clean_line)
                if correspondencia_at_1:
                    valor_a_str = correspondencia_at_1.group(2)
                    valor_a = valor_a_str.replace('B', '')
                    estado_sequencia_at = 1
                    
            elif estado_sequencia_at == 1:
                correspondencia_at_2 = padrao_at_linha2.search(clean_line)
                if correspondencia_at_2:
                    valor_b = correspondencia_at_2.group(2)
                    asm_lib.atribuicao_simples(valor_a,valor_b,outfile)
                    estado_sequencia_at = 0

            #|SALTOS|
            padrao_s = re.compile(r'^\s*goto\s*<(\w+)\.(\d+)>\s*;?$')
            correspondencia_s = padrao_s.search(clean_line)

            if correspondencia_s:
                label_letra = correspondencia_s.group(1)
                label_numero = correspondencia_s.group(2)
                asm_lib.salto(label_letra,label_numero,outfile)
            
            #|CHAMADAS DE FUNÇAO|
            padrao_ch = re.compile(r'(\w+_\w+)\s*\(\s*\);')
            correspondencia_ch = padrao_ch.search(clean_line)

            if correspondencia_ch:
                funcao = correspondencia_ch.group(1)
                funcao_maiusculo = funcao.upper()
                asm_lib.chamada_de_funcao(funcao_maiusculo,outfile)
            
            #|DEFINIÇAO DE PONTEIRO|
            #Tipo e nome do ponteiro
            padrao_dfp = re.compile(r'(?:volatile\s)?(long\s)?(int)\s(\w+)\s*;')
            correspondencia_dfp = padrao_dfp.search(clean_line)
            
            if correspondencia_dfp:
                long_prefixo = correspondencia_dfp.group(1)
                tipo_base = correspondencia_dfp.group(2)
                nome_p = correspondencia_dfp.group(3)
                if long_prefixo:
                    tipo_p = 'long ' + tipo_base
                else:
                    tipo_p = tipo_base
                variaveis_codigo['ponteiro'] = {'nome':nome_p,'tipo':tipo_p}

            #Endereco do ponteiro
            padrao_dfp0 = re.compile(rf'{variaveis_codigo['ponteiro']['nome']}\s*=\s*(\d+)\s*;')
            correspondencia_dfp0 = padrao_dfp0.search(clean_line)

            if correspondencia_dfp0:
                endereco_string = correspondencia_dfp0.group(1)
                endereco = int(endereco_string)
                variaveis_codigo['ponteiro']['endereço'] = endereco_string
                asm_lib.define_ponteiro(nome_p,tipo_p,endereco,outfile)
            #Limpeza do ponteiro
                asm_lib.clear_ponteiro(variaveis_codigo['ponteiro']['nome'],variaveis_codigo['ponteiro']['tipo'],outfile)
                
            #|INCREMENTO DO PONTEIRO|
            padrao_inc_linha1 = re.compile(rf'{variaveis_codigo['ponteiro']['nome']}\.(\d+_\d+)\s*=\s*{variaveis_codigo['ponteiro']['nome']}\s*;')
            padrao_inc_linha2 = re.compile(rf'_(\d+)\s*=\s*{variaveis_codigo['ponteiro']['nome']}\.(\d+_\d+)\s*\+\s*(\d+)\s*;')
            padrao_inc_linha3 = re.compile(rf'{variaveis_codigo['ponteiro']['nome']}\s*=\s*_(\d+)\s*;')
            
            if estado_sequencia_inc == 0:
                if padrao_inc_linha1.search(clean_line):
                   estado_sequencia_inc = 1

            elif estado_sequencia_inc == 1:
                 if padrao_inc_linha2.search(clean_line):
                    estado_sequencia_inc = 2

            elif estado_sequencia_inc == 2:
                if padrao_inc_linha3.search(clean_line):
                    asm_lib.incremento_ponteiro(variaveis_codigo['ponteiro']['nome'],variaveis_codigo['ponteiro']['tipo'],outfile)  
                    # Reset o estado para procurar uma nova sequencia
                    estado_sequencia_inc = 0
            
            #|CONDICIONAL|
            padrao_cond_linha1 = re.compile(r'i\.(\d+_\d+)\s*=\s*i\s*;')
            padrao_cond_linha2 = re.compile(r'if\s*\(([\w.]+)\s*<=\s*(\d+)\)\s*goto\s*<([\w.]+?)>;?\s*else\s*goto\s*<([\w.]+?)>;?')

            if estado_sequencia_cond == 0:
                if padrao_cond_linha1.search(clean_line):
                    estado_sequencia_cond = 1
            elif estado_sequencia_cond == 1:
                correspondencia_cond = padrao_cond_linha2.search(clean_line)
                if correspondencia_cond:
                    valor_condicional = correspondencia_cond.group(2)
                    goto_true = correspondencia_cond.group(3)
                    goto_false = correspondencia_cond.group(4)

                    goto_true_limpo = goto_true.replace('.', '')
                    goto_false_limpo = goto_false.replace('.', '')
                    variaveis_codigo['label']['para ignorar'] = goto_false

                    asm_lib.condicional(variaveis_codigo['ponteiro']['nome'],valor_condicional,goto_true_limpo,variaveis_codigo['ponteiro']['tipo'],outfile)

                    estado_sequencia_cond = 0
        
        #|FIM DO PROGRMA|            
        outfile.write('\n        END')
        
            # =========================================================

except FileNotFoundError:
    print(f"ERRO: O arquivo '{gimple_filename}' nao foi encontrado!")
    print("Verifique se o nome do arquivo (incluindo o numero) esta correto.")

print("--- Arquivo assembly gerado ---\n")

#|||FIM DO PARSING ASM|||
# ==================================================================================================================================================================


# ==================================================================================================================================================================
#|||GERAÇAO DE ARQUIVO .HEX COM BASE NO INTEL HEX 8|||

# ==============================================================================
# 1. FUNÇÕES AUXILIARES (PARSING E BUSCA)
# ==============================================================================

def parse_line(line_text):
    """
    Versão refinada que diferencia Labels de Símbolos (EQU).
    """
    code_part = line_text.split(';')[0].strip()
    if not code_part:
        return None

    # Etapa 1: Processa APENAS labels de endereço (com ':')
    label = None
    if ':' in code_part:
        parts = code_part.split(':', 1)
        label = parts[0].strip().upper()
        code_part = parts[1].strip()

    if not code_part:
        return {'label': label, 'instruction': None, 'operands': []}

    instruction_parts = code_part.replace(',', ' ').split()
    if not instruction_parts:
        return {'label': label, 'instruction': None, 'operands': []}

    # Etapa 2: Processa a instrução e os operandos
    instruction = None
    operands = []

    # Tratamento da sintaxe 'NOME EQU VALOR'
    if len(instruction_parts) > 1 and instruction_parts[1].upper() == 'EQU':
        # A instrução é 'EQU'. O nome (i0) e o valor (0x0) são seus operandos.
        instruction = 'EQU'
        # O 'label' de endereço (com ':') não é modificado.
        # Guardamos o símbolo como o primeiro operando.
        operands = [instruction_parts[0]] + instruction_parts[2:]

    else:
        # Lógica padrão para todas as outras instruções
        instruction = instruction_parts[0]
        operands = instruction_parts[1:]

    # Converte para maiúsculas no final para garantir consistência
    instruction_upper = instruction.upper()
    operands_upper = [op.upper() for op in operands]

    return {'label': label, 'instruction': instruction_upper, 'operands': operands_upper}

def obter_endereco_por_label(label_procurado, programa):
    """
    Encontra o endereço associado a um label de forma não sensível ao caso.
    """
    if label_procurado is None:
        return None
    
    label_procurado_upper = label_procurado.upper()

    for i, linha in enumerate(programa):
        if linha['label'] == label_procurado_upper:
            if linha['address'] is not None:
                return linha['address']
            for j in range(i + 1, len(programa)):
                proxima_linha = programa[j]
                if proxima_linha['address'] is not None:
                    return proxima_linha['address']
    return None

# ==============================================================================
# 2. LÓGICA PRINCIPAL (LER E PROCESSAR O ARQUIVO)
# ==============================================================================

asm_filename = "LED_BlinkC.c.007t.asm"
programa_parseado = []
DIRETIVAS = {'LIST', 'INCLUDE', 'CONFIG', 'EQU', 'END'}
addr_instruction = 0
contador_linhas_validas = 0

print(f"--- Iniciando análise do arquivo: {asm_filename} ---")

try:
    with open(asm_filename, 'r', encoding='utf-8') as infile:
        for line_asm in infile:
            clean_line_asm = line_asm.strip()
            if not clean_line_asm:
                continue

            contador_linhas_validas += 1
            parsed_data = parse_line(clean_line_asm)

            if not parsed_data:
                continue
            
            # Adiciona o número da linha e o código original aos dados parseados
            parsed_data['line_number'] = contador_linhas_validas
            parsed_data['raw_code'] = clean_line_asm
            
            instruction = parsed_data['instruction']
            
            if instruction in DIRETIVAS:
                parsed_data['address'] = None
                programa_parseado.append(parsed_data)
                continue
            elif instruction == 'ORG':
                addr_instruction = int(parsed_data['operands'][0], 0)
                parsed_data['address'] = None
                programa_parseado.append(parsed_data)
                continue
            elif instruction is None:
                # Linha apenas com label
                parsed_data['address'] = None
                programa_parseado.append(parsed_data)
                continue
            else:
                parsed_data['address'] = addr_instruction
                programa_parseado.append(parsed_data)
                
                if instruction in ['GOTO', 'CALL']:
                    addr_instruction += 2
                else:
                    addr_instruction += 1

except FileNotFoundError:
    print(f"ERRO: O arquivo '{asm_filename}' não foi encontrado.")

print("--- Análise concluída ---")


# ==============================================================================
# 3. PRÉ-PROCESSAMENTO (CRIAR TABELA DE SÍMBOLOS)
# ==============================================================================

#print("\n--- Criando Tabelas de Símbolos e Constantes ---")
tabela_de_simbolos = {}
tabela_de_constantes = {
    'STATUS': 0xFD8,
    'Z': 2
}

for linha in programa_parseado:
    # Popula a tabela de labels de endereço (para GOTO/CALL)
    if linha['label']:
        endereco = obter_endereco_por_label(linha['label'], programa_parseado)
        tabela_de_simbolos[linha['label']] = endereco

    # Popula a nova tabela de constantes (para EQU)
    if linha['instruction'] == 'EQU':
        nome_constante = linha['operands'][0]
        valor_constante = int(linha['operands'][1], 0) # Converte o valor para inteiro
        tabela_de_constantes[nome_constante] = valor_constante

#print("--- Tabelas criadas com sucesso ---")
#print("\nLabels de Endereço:")
#pprint.pprint(tabela_de_simbolos)
#print("\nConstantes (EQU):")
#pprint.pprint(tabela_de_constantes)

# ==============================================================================
# 4. GERAÇÃO DE OPCODE
# ==============================================================================

print("\n--- Gerando lista com o Opcode das instruçoes ---")

with open('opcode_list.txt', 'w') as arquivo:
    for linha in programa_parseado:
        if linha['address'] is None:
            continue # Pula diretivas e labels sozinhos

        opcode_simulado = "????" # Valor padrão
        address = linha['address']
        instrucao = linha['instruction']
        operandos = linha['operands']

        if instrucao == 'CALL':
            label_alvo = operandos[0]
            endereco_alvo = tabela_de_simbolos.get(label_alvo)
            hex_lib.call_hex(address,endereco_alvo,arquivo)
    
        elif instrucao == 'MOVWF':
            hex_lib.movwf_hex(address,operandos,tabela_de_constantes,arquivo)

        elif instrucao == 'MOVLW':
            hex_lib.movlw_hex(address,operandos,arquivo)
    
        elif instrucao == 'GOTO':
            label_alvo = operandos[0]
            endereco_alvo = tabela_de_simbolos.get(label_alvo)
            hex_lib.goto_hex(address, endereco_alvo,arquivo)

        elif instrucao == 'RETURN':
            hex_lib.return_hex(address,arquivo)
    
        elif instrucao == 'XORLW':
            hex_lib.xorlw_hex(address,operandos,arquivo)

        elif instrucao == 'MOVF':
            hex_lib.movf_hex(address, operandos, tabela_de_constantes,arquivo)

        elif instrucao == 'INCF':
            hex_lib.incf_hex(address, operandos, tabela_de_constantes,arquivo)

        elif instrucao == 'BTFSC':
            hex_lib.btfsc_hex(address, operandos, tabela_de_constantes,arquivo)

        elif instrucao == 'CLRF':
            hex_lib.clrf_hex(address, operandos, tabela_de_constantes,arquivo)

        elif instrucao == 'BNZ':
            hex_lib.bnz_hex(address, operandos, tabela_de_simbolos,arquivo)

        elif instrucao == 'BRA':
            hex_lib.bra_hex(address, operandos, tabela_de_simbolos,arquivo)

print("--- Lista gerada ---")

print(f"\n--- Conversao do arquivo '{'opcode_list.txt'}' para o formato Intel Hex8 ---")

hex_lib.gerar_arquivo_hex('opcode_list.txt','LED_Blink.hex')