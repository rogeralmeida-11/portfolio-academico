#hex_lib

#|||GERADOR DE OPCODE DAS INSTRUÇOES|||

#MOVWF 0110 111A FFFF FFFF
def movwf_hex(address, operandos, tabela_de_constantes,arquivo):
 
    address_hex = f"{address:04X}"

    try:
        # --- Passo 1: Decodificar os operandos ---
        nome_registrador = operandos[0]
        
        # 'a' (ACCESS ou BANKED) é opcional. Padrão é ACCESS (a=0).
        access_bit_str = 'ACCESS'
        if len(operandos) > 1:
            access_bit_str = operandos[1]

        # --- Passo 2: Resolver o endereço do registrador 'f' ---
        f_valor = 0
        if nome_registrador in tabela_de_constantes:
            f_valor = tabela_de_constantes[nome_registrador]
        else:
            # Se não for um símbolo, deve ser um endereço literal como '0xF93'
            f_valor = int(nome_registrador, 0)
        
        # O opcode usa apenas os 8 bits baixos do endereço
        f_8bit = f_valor & 0xFF

        # --- Passo 3: Montar o opcode ---
        # Formato: 0110 111a ffff ffff
        
        # O primeiro byte é 6E para ACCESS (a=0) ou 6F para BANKED (a=1)
        primeiro_byte = 0x6E if access_bit_str == 'ACCESS' else 0x6F
        
        # Juntando o primeiro byte com o endereço de 8 bits
        opcode = (primeiro_byte << 8) | f_8bit
        
        opcode_str = f"{opcode:04X}"
        arquivo.write(f"{address_hex} {opcode_str}\n")

    except (IndexError, ValueError, KeyError) as e:
        print(f"\t-> ERRO de sintaxe ou símbolo não encontrado em {address_hex} para MOVWF: {e}")

#MOVLW 0000 1110  KKKK KKKK == 0EKK
def movlw_hex(address, operandos,arquivo):
    
    address_hex = f"{address:04X}"

    try:
        # Pega o primeiro operando, que é a string do valor literal (ex: '0xfc')
        k_str = operandos[0]

        # Converte a string hexadecimal em um número inteiro
        k_int = int(k_str, 0)
        
        # Formata o número para 2 dígitos hexadecimais
        k_hex_formatado = f"{k_int:02X}"
        
        # Monta o opcode final: 0E seguido do valor
        opcode_str = f"0E{k_hex_formatado}"

        arquivo.write(f"{address_hex} {opcode_str}\n")

    except (IndexError, ValueError) as e:
        print(f"# ERRO de sintaxe em {address_hex} para MOVLW: {e}")
    
#CALL 1110 110S KKKK KKKK => K LOW BITS  [S == 0(default)]
#     1111 KKKK KKKK KKKK => K HIGH BITS
def call_hex(address, address_label,arquivo):
    
    address_hex = f"{address:04X}" # Endereço da própria instrução CALL

    # Primeiro, verifique se o endereço do label foi encontrado
    if address_label is not None:
        # 'address_label' é o nosso endereço de destino K (ex: 27)
        K = address_label

        # --- Passo 1: Isolar as partes do endereço K ---
        
        # Para pegar os 8 bits baixos (KKKK KKKK), usamos uma máscara & 0xFF
        k_low_8bits = K & 0xFF

        # Para pegar os 12 bits altos, deslocamos K 8 bits para a direita (>>)
        # e depois aplicamos uma máscara & 0xFFF para garantir que temos apenas 12 bits.
        k_high_12bits = (K >> 8) & 0xFFF

        # --- Passo 2: Montar as duas palavras do opcode ---

        # Primeira palavra: 1110 1100 (EC) + 8 bits baixos de K
        # 0xEC00 é a base, e usamos o OU bitwise (|) para adicionar os bits do endereço
        opcode_word1 = 0xEC00 | k_low_8bits

        # Segunda palavra: 1111 (F) + 12 bits altos de K
        # 0xF000 é a base, e usamos o OU bitwise (|) para adicionar os bits do endereço
        opcode_word2 = 0xF000 | k_high_12bits
        
        # --- Passo 3: Imprimir o resultado formatado ---
        
        arquivo.write(f"{address_hex} {opcode_word1:04X}\n")
        arquivo.write(f"{address_hex} {opcode_word2:04X}\n")

    else:
        # Se o endereço não foi encontrado, imprima um erro claro
        print(f"\t-> ERRO em {address_hex}: O endereço do label para o CALL não foi encontrado!")

#GOTO 1110 1111 KKKK KKKK => K LOW BITS
#     1111 KKKK KKKK KKKK => K HIGH BITS
def goto_hex(address, address_label,arquivo):
    
    address_hex = f"{address:04X}" # Endereço da própria instrução GOTO

    # Verifique se o endereço do label foi encontrado
    if address_label is not None:
        # 'address_label' é o nosso endereço de destino K
        K = address_label

        # --- Isolar as partes do endereço K ---
        k_low_8bits = K & 0xFF
        k_high_12bits = (K >> 8) & 0xFFF

        # --- Montar as duas palavras do opcode ---
        
        # Primeira palavra: 1110 1111 (EF) + 8 bits baixos de K
        # A ÚNICA DIFERENÇA DO CALL ESTÁ AQUI: 0xEF00
        opcode_word1 = 0xEF00 | k_low_8bits

        # Segunda palavra: 1111 (F) + 12 bits altos de K (idêntico ao CALL)
        opcode_word2 = 0xF000 | k_high_12bits
        
        arquivo.write(f"{address_hex} {opcode_word1:04X}\n")
        arquivo.write(f"{address_hex} {opcode_word2:04X}\n")

    else:
        # Se o endereço não foi encontrado, imprima um erro claro
        print(f"\t-> ERRO em {address_hex}: O endereço do label para o GOTO não foi encontrado!")

#RETURN 0000 0000 0001 001S
def return_hex(address,arquivo):
    address_hex = f"{address:04X}"
    arquivo.write(f'{address_hex} 0012\n')

#XORLW 0000 1010 KKKK KKKK == 0AKK
def xorlw_hex(address,params,arquivo):
    address_hex = f"{address:04X}"
    K = params[0]
    K_int = int(K,0)
    K_hex = f"{K_int:02X}"
    arquivo.write(f'{address_hex} 0A{K_hex}\n')

#MOVF 0101 00DA FFFF FFFF
def movf_hex(address_instr,params_instr,tabela_de_constantes,arquivo):
    address_hex = f"{address_instr:04X}"
    nome_registrador = params_instr[0]
    if nome_registrador in tabela_de_constantes:
        F = tabela_de_constantes[nome_registrador]
    else:
        F = int(nome_registrador,0)
    
    F_hex = f"{F:02X}"
    if params_instr[1] == 'W' and params_instr[2] == 'ACCESS':  #[D=0 e A=0]
            arquivo.write(f'{address_hex} 50{F_hex}\n')

#INCF 0010 10DA FFFF FFFF
def incf_hex(address_instr,params_instr,tabela_de_constantes,arquivo):
    address_hex = f"{address_instr:04X}"
    nome_registrador = params_instr[0]
    if nome_registrador in tabela_de_constantes:
        F = tabela_de_constantes[nome_registrador]
    else:
        F = int(nome_registrador,0)
    
    F_hex = f"{F:02X}"
    if params_instr[1] == 'F' and params_instr[2] == 'ACCESS':  #[D=1 e A=0]
            arquivo.write(f'{address_hex} 2A{F_hex}\n')

#BTFSC 1011 BBBA FFFF FFFF
def btfsc_hex(address, operandos, tabela_de_constantes,arquivo):
    
    address_hex = f"{address:04X}"

    try:
        # --- Passo 1: Decodificar os operandos ---
        
        # 'f' é o primeiro operando (o registrador)
        nome_registrador = operandos[0]
        if nome_registrador in tabela_de_constantes:
            # Pega o endereço de 12 bits de STATUS (0xFD8)
            f_full = tabela_de_constantes[nome_registrador]
            # O opcode usa apenas os 8 bits baixos do endereço para ACCESS bank
            f = f_full & 0xFF # Resultado será 0xD8
        else:
            f = int(nome_registrador, 0)

        # 'b' é o segundo operando (o bit)
        nome_bit = operandos[1]
        if nome_bit in tabela_de_constantes:
            b = tabela_de_constantes[nome_bit] # Pega o valor 2 de 'Z'
        else:
            b = int(nome_bit, 0)
        
        # O operando 'a' (ACCESS/BANKED) é ignorado neste modelo simplificado,
        # pois já assumimos o uso do access bank ao pegar os 8 bits de 'f'.

        # --- Passo 2: Montar o opcode ---
        # Formato: 1011 bbb1 ffff ffff
        
        # Primeiro byte: 0xB1 + (b * 2)
        opcode_byte1 = 0xB0 + (b * 2) ######################## MUDANÇA PARA FICAR IGUAL AO DO MPASM (TROCA BTFSC POR BTFSS)
        
        # Segundo byte: f
        opcode_byte2 = f
        
        # Juntando os dois bytes para formar a palavra de 16 bits
        opcode = (opcode_byte1 << 8) | opcode_byte2
        
        opcode_str = f"{opcode:04X}"
        arquivo.write(f"{address_hex} {opcode_str}\n")

    except (IndexError, ValueError, KeyError) as e:
        print(f"\t-> ERRO de sintaxe ou símbolo não encontrado em {address_hex} para BTFSC: {e}")

#CLRF 0110 101A FFFF FFFF
def clrf_hex(address_instr,params_instr,tabela_de_constantes,arquivo):
    address_hex = f"{address_instr:04X}"
    nome_registrador = params_instr[0]
    if nome_registrador in tabela_de_constantes:
        F = tabela_de_constantes[nome_registrador]
    else:
        F = int(nome_registrador,0)
    
    F_hex = f"{F:02X}"
    if params_instr[1] == 'ACCESS':  #[A=0]
            arquivo.write(f'{address_hex} 6A{F_hex}\n')

#BNZ 1110 0001 NNNN NNNN == E1NN
def bnz_hex(address, operandos, tabela_de_simbolos,arquivo):
    
    address_hex = f"{address:04X}"

    try:
        # --- Passo 1: Encontrar o endereço de destino ---
        label_alvo = operandos[0]
        endereco_alvo = tabela_de_simbolos.get(label_alvo)

        if endereco_alvo is None:
            print(f"\t-> ERRO em {address_hex}: O label '{label_alvo}' para o BNZ não foi encontrado!")
            return

        # --- Passo 2: Calcular o deslocamento relativo 'n' ---
        # Fórmula: n = Endereço_Destino - (Endereço_Atual + 1)
        # O '+1' representa o endereço da instrução seguinte.
        n = endereco_alvo - (address + 1)

        # --- Passo 3: Montar o opcode ---
        # Primeiro byte fixo é 0xE2
        opcode_byte1 = 0xE1 ##################################### MUDANÇA PARA FICAR IGUAL AO DO MPASM (TROCA BNZ POR BN)
        
        # O segundo byte é o deslocamento 'n' em formato de 8 bits.
        # A máscara & 0xFF lida com o complemento de dois para números negativos.
        opcode_byte2 = n & 0xFF
        
        opcode = (opcode_byte1 << 8) | opcode_byte2
        
        opcode_str = f"{opcode:04X}"
        arquivo.write(f"{address_hex} {opcode_str}\n")

    except (IndexError, ValueError) as e:
        print(f"\t-> ERRO de sintaxe em {address_hex} para BNZ: {e}")

#BRA 1101 0NNN NNNN NNNN
def bra_hex(address, operandos, tabela_de_simbolos,arquivo):
   
    address_hex = f"{address:04X}"

    try:
        # --- Passo 1: Encontrar o endereço de destino ---
        label_alvo = operandos[0]
        endereco_alvo = tabela_de_simbolos.get(label_alvo)

        if endereco_alvo is None:
            print(f"\t-> ERRO em {address_hex}: O label '{label_alvo}' para o BRA não foi encontrado!")
            return

        # --- Passo 2: Calcular o deslocamento relativo 'n' ---
        # A fórmula é a mesma do BNZ
        n = endereco_alvo - (address + 1)

        # --- Passo 3: Montar o opcode ---
        # A base do opcode é 0xD000 (para 1101 0...)
        opcode_base = 0xD000
        
        # O deslocamento 'n' deve ser de 11 bits.
        # A máscara & 0x7FF garante o complemento de dois para 11 bits.
        n_11bit = n & 0x7FF
        
        # Juntamos a base com o deslocamento
        opcode = opcode_base | n_11bit
        
        opcode_str = f"{opcode:04X}"
        arquivo.write(f"{address_hex} {opcode_str}\n")

    except (IndexError, ValueError) as e:
        print(f"\t-> ERRO de sintaxe em {address_hex} para BRA: {e}")

#GERA ARQUIVO FINAL .HEX
def gerar_arquivo_hex(arquivo_de_entrada, arquivo_de_saida):

    # --- Funções Auxiliares ---

    def swap_endianness(opcode_str):
        swapped = ""
        for i in range(0, len(opcode_str), 4):
            word = opcode_str[i:i+4]
            if len(word) == 4:
                low_byte, high_byte = word[2:4], word[0:2]
                swapped += low_byte + high_byte
        return swapped

    def calcular_checksum(byte_string):
        soma = 0
        for i in range(0, len(byte_string), 2):
            soma += int(byte_string[i:i+2], 16)
        return (~soma + 1) & 0xFF

    def criar_registro_hex(endereco, dados_str):
        if not dados_str:
            return None
        byte_count = len(dados_str) // 2
        record_type = '00'
        checksum_data = f'{byte_count:02X}{endereco:04X}{record_type}{dados_str}'
        checksum = calcular_checksum(checksum_data)
        return f':{checksum_data}{checksum:02X}'.upper()

    # --- Início da Lógica Principal da Função ---

    # FASE 1: LER E JUNTAR OS DADOS DO ARQUIVO DE ENTRADA
    dados_por_endereco = {}
    try:
        with open(arquivo_de_entrada, 'r') as f_in:
            for linha_texto in f_in:
                partes = linha_texto.strip().split()
                if len(partes) < 2: continue
                try:
                    endereco = int(partes[0], 16)
                    opcode_parte = "".join(partes[1:])
                    int(opcode_parte, 16)
                    if endereco in dados_por_endereco:
                        dados_por_endereco[endereco] += opcode_parte
                    else:
                        dados_por_endereco[endereco] = opcode_parte
                except ValueError:
                    print(f"Aviso: Linha ignorada por conter dados inválidos -> '{linha_texto.strip()}'")
                    continue
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_de_entrada}' não foi encontrado.")
        return False # Retorna False em caso de falha

    # FASE 2: GERAR OS REGISTROS HEX A PARTIR DOS DADOS JUNTADOS
    if not dados_por_endereco:
        print("Nenhuma instrução válida encontrada no arquivo de entrada.")
        return False

    registros_hex = [':020000040000FA']
    enderecos_ordenados = sorted(dados_por_endereco.keys())
    
    dados_completos_str = ""
    for endereco in enderecos_ordenados:
        dados_completos_str += swap_endianness(dados_por_endereco[endereco])

    endereco_byte_inicial = enderecos_ordenados[0] * 2
    tamanho_chunk_hex = 32

    for i in range(0, len(dados_completos_str), tamanho_chunk_hex):
        chunk_de_dados = dados_completos_str[i : i + tamanho_chunk_hex]
        endereco_do_chunk = endereco_byte_inicial + (i // 2)
        registro = criar_registro_hex(endereco_do_chunk, chunk_de_dados)
        registros_hex.append(registro)

    linhas_config_final = [
        ':020000040030CA',
        ':03000100C10F1E0E',
        ':020005008081F8',
        ':0600080003C003E0034009'
    ]
    registros_hex.extend(linhas_config_final)
    registros_hex.append(':00000001FF')

    with open(arquivo_de_saida, 'w', newline='\r\n') as f_out:
        for registro in registros_hex:
            f_out.write(registro.upper() + '\n')
            
    print(f"--- Conversão concluída. Arquivo '{arquivo_de_saida}' gerado com sucesso! ---")
    return True # Retorna True em caso de sucesso