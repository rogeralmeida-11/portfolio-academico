#asm_lib.py

def config_pic(outfile):
    outfile.write('        LIST    P=18F1220\n')
    outfile.write('        INCLUDE <p18f1220.inc>\n')
    outfile.write('        CONFIG OSC = XT\n')
    outfile.write('        CONFIG WDT = OFF\n')
    outfile.write('        CONFIG LVP = OFF\n\n')

def define_ponteiro(i,type,f,outfile): #i=k
    
    if (type == 'long int'):
        outfile.write(f'        {i}0 EQU {hex(f)}\n')
        outfile.write(f'        {i}1 EQU {hex(f+1)}\n')
        outfile.write(f'        {i}2 EQU {hex(f+2)}\n')
        outfile.write(f'        {i}3 EQU {hex(f+3)}\n')
    elif (type == 'int'):
        outfile.write(f'        {i}0 EQU {hex(f)}\n')
        outfile.write(f'        {i}1 EQU {hex(f+1)}\n')

def clear_ponteiro(i,type,outfile):
    if (type == 'long int'):
        outfile.write(f'        CLRF {i}0, ACCESS\n')
        outfile.write(f'        CLRF {i}1, ACCESS\n')
        outfile.write(f'        CLRF {i}2, ACCESS\n')
        outfile.write(f'        CLRF {i}3, ACCESS\n')
    elif (type == 'int'):
        outfile.write(f'        CLRF {i}0, ACCESS\n')
        outfile.write(f'        CLRF {i}1, ACCESS\n')

def incremento_ponteiro(i,type,outfile):
    if (type == 'long int'):
        outfile.write(f'        INCF {i}0, F, ACCESS\n')
        outfile.write('        BTFSC STATUS, Z\n')
        outfile.write(f'        INCF {i}1, F, ACCESS\n')
        outfile.write('        BTFSC STATUS, Z, ACCESS\n')
        outfile.write(f'        INCF {i}2, F, ACCESS\n')
        outfile.write('        BTFSC STATUS, Z, ACCESS\n')
        outfile.write(f'        INCF {i}3, F, ACCESS\n')

    elif (type == 'int'):
        outfile.write(f'        INCF {i}0, F,ACCESS\n')
        outfile.write('        BTFSC STATUS, Z, ACCESS\n')
        outfile.write(f'        INCF {i}1, F, ACCESS\n')

def atribuicao_simples(valor_a,valor_b,outfile): #p=a e *p=b
    valor_a_int = int(valor_a)
    valor_b_int = int(valor_b)
    outfile.write(f'        MOVLW {hex(valor_b_int)}\n')
    outfile.write(f'        MOVWF {hex(valor_a_int)}, ACCESS\n')

def condicional(i,k,label_inc,type,outfile):
    k_int = int(k)
    byte0 = k_int & 0xFF          # Pega os 8 bits mais baixos (0-7)
    byte1 = (k_int >> 8) & 0xFF   # Pega os bits 8-15
    byte2 = (k_int >> 16) & 0xFF  # Pega os bits 16-23
    byte3 = (k_int >> 24) & 0xFF
    
    if type == 'long int':
        # Compara o byte mais significativo (byte 3)
        outfile.write(f'        MOVF {i}3, W, ACCESS\n')
        outfile.write(f'        XORLW {hex(byte3)}\n')
        outfile.write(f'        BNZ {label_inc}\n\n')

        # Compara o byte 2
        outfile.write(f'        MOVF {i}2, W, ACCESS\n')
        outfile.write(f'        XORLW {hex(byte2)}\n')
        outfile.write(f'        BNZ {label_inc}\n\n')

        # Compara o byte 1
        outfile.write(f'        MOVF {i}1, W, ACCESS\n')
        outfile.write(f'        XORLW {hex(byte1)}\n')
        outfile.write(f'        BNZ {label_inc}\n\n')
        
        # Compara o byte menos significativo (byte 0)
        outfile.write(f'        MOVF {i}0, W, ACCESS\n')
        outfile.write(f'        XORLW {hex(byte0)}\n')
        outfile.write(f'        BNZ {label_inc}\n\n')
        outfile.write('\n        RETURN\n')
        
    elif type == 'int':
        outfile.write(f'        MOVF {i}1, W, ACCESS\n')
        outfile.write(f'        XORLW {hex(byte1)}\n')
        outfile.write(f'        BNZ {label_inc}\n')
        
        outfile.write(f'        MOVF {i}0, W, ACCESS\n')
        outfile.write(f'        XORLW {hex(byte0)}\n')
        outfile.write(f'        BNZ {label_inc}\n')
        outfile.write('\n        RETURN\n')

def salto(label_l,label_n,outfile):
    outfile.write(f'        BRA {label_l}{label_n}\n')

def chamada_de_funcao(funcao,outfile):
    outfile.write(f'        CALL {funcao}\n')

def label_simples(label_l,label_n,outfile):
    outfile.write(f'{label_l}{label_n}:\n')

def label_de_funcoes(lb_function,outfile):
    outfile.write(f'{lb_function}:\n')