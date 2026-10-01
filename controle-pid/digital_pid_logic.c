#include <18f1220.h>
#fuses XT,NOWDT,NOMCLR,NOPROTECT,NOLVP,NOBROWNOUT
#use delay (clock=4000000)

int32 u;
int32 z;
int32 zP;
int32 e;
int32 eP;
int32 eP2;
int32 Sp;
int32 sensor_r;
unsigned int8 iAdd;

// --- 1. Definição dos Estados da Máquina ---
typedef enum 
{
    INITIALIZATION,
    RUN,
    MANUAL,
    SAFE
} SystemState_e;

// --- 2. Variável de Estado Global ---
volatile SystemState_e estado_atual;
volatile int1 flag_executa_pid = FALSE; // Flag para o Timer

// --- Protótipos das Funções ---
// Função da lógica de transição dos estados
SystemState_e evalTransition(void);

// Funções que executam as ações dos estados
void exec_initialization(void);
void exec_run(void);
void exec_manual(void);
void exec_safe(void);

// Funções para ler as condições
int1 check_manual_condition(void);
int1 check_fault_condition(void);
int1 check_reset_condition(void);


#INT_TIMER1
void timer1_isr() 
{
    set_timer1(40536); // Recarrega o timer para a próxima interrupção
    flag_executa_pid = TRUE; // Sinaliza que é hora de rodar o PID
}

//=============================================================================
//  FUNÇÃO PRINCIPAL (MAIN)
//=============================================================================
void main() {

    //Tempo de amostragem definido para 25ms
    set_timer1(40536);
    setup_timer_1(T1_INTERNAL|T1_DIV_BY_1);
    enable_interrupts(INT_TIMER1);
    enable_interrupts(GLOBAL);
    
    // Define o estado inicial do sistema
    estado_atual = INITIALIZATION;
    
    setup_adc_ports(NO_ANALOGS);
    set_tris_a(0b00011111);
    set_tris_b(0b10100000);
    
    while(1)
    {
        // Executa a ação correspondente ao NOVO estado.
        switch(estado_atual) 
        {
            case INITIALIZATION:
                output_high(PIN_B0);
                exec_initialization();
                delay_ms(100);
                output_low(PIN_B0);
                if (input(PIN_A4)){u=255;}
                break;

            case RUN:
                
                if (flag_executa_pid) 
                {
                   output_high(PIN_B1);
                   exec_run();
                   flag_executa_pid = FALSE;
                   output_low(PIN_B1);
                }
                
                break;

            case MANUAL:
                output_high(PIN_B2);
                exec_manual();
                output_low(PIN_B2);
                break;

            case SAFE:
                output_high(PIN_B3);
                exec_safe();
                output_low(PIN_B3);
                break;
        }
        
        estado_atual = evalTransition(); //Avalia as transições e atualiza o estado atual.
    }
}



//=============================================================================
//  IMPLEMENTAÇÃO DA LÓGICA DE TRANSIÇÃO
//=============================================================================
SystemState_e evalTransition(void) 
{
    SystemState_e proximo_estado = estado_atual; // Por padrão, permanece no mesmo estado.

    switch(estado_atual) 
    {
        case INITIALIZATION:
//!            if (input(PIN_A4)) 
//!            
//!            {
//!                
//!                proximo_estado = SAFE;           
//!            }
            if (check_fault_condition())
            {
                proximo_estado = SAFE;
            } 
            else if (check_manual_condition())
            {
                proximo_estado = MANUAL;
            }
            else proximo_estado = RUN;
            break;

        case RUN:
            // Verifica as condições de saída do modo RUN
            if (check_fault_condition()) 
            {
                proximo_estado = SAFE;
            } 
            else if (check_manual_condition())
            {
                proximo_estado = MANUAL;
            }
            // Se nenhuma condição for atendida, ele permanece em RUN (valor padrão).
            break;

        case MANUAL:
            // Verifica as condições de saída do modo MANUAL
            if (check_fault_condition()) 
            {
                proximo_estado = SAFE;
            } 
            else if (!check_manual_condition()) // Se o modo manual foi desativado
            { 
                proximo_estado = RUN;
            }
            // Se nenhuma condição for atendida, permanece em MANUAL.
            break;

        case SAFE:
            // A única forma de sair do modo SAFE é com um reset.
            if (check_reset_condition()) 
            {
                proximo_estado = INITIALIZATION;
            }
            // Se não, permanece em SAFE para sempre.
            break;
    }
    return proximo_estado;
}


//=============================================================================
//  IMPLEMENTAÇÃO DAS AÇÕES DE CADA ESTADO
//=============================================================================


void exec_initialization() 
{
    u=0;
    z=0;
    zP=0;
    e=0;
    eP=0;
    eP2=0;
    Sp=50;
    sensor_r=20;
    iAdd=0;
}


void exec_run()
{
   //Cálculo do PID
   e=Sp-sensor_r;
   z=zP+(41*e)-(72*eP)+(32*eP2); //Equaçao de recorrencia do PID para Kp=1 Ki=5 Kd=0.1 Ts=25ms
   u=z>>3;

   zP=z;
   eP2=eP;
   eP=e;
   
   if (u>=255){u=255;}
   
   write_eeprom(iAdd,u);
   iAdd ++;
}


void exec_manual(void) 
{
    if (input(PIN_A0)) //100%
    {
       u=255;
    }
    else if (input(PIN_A1)) //75%
    {
       u=191;
    }
    else if (input(PIN_A2)) //50%
    {
       u=127;
    }
    else if (input(PIN_A3)) //25%
    {
       u=63;
    }
    
    write_eeprom(iAdd,u);
    iAdd++;
}


void exec_safe(void) 
{
    u=0;
    z=0;    
    zP=0;    
    e=0;    
    eP=0;
    eP2=0;
    
    write_eeprom(iAdd,u);
    iAdd ++; 
}

//// Funções de leitura de condição
int check_manual_condition(void) {return (input(PIN_B7));}
int check_fault_condition(void) {return (u>=255);}
int check_reset_condition(void)  {return (input(PIN_B5));}


