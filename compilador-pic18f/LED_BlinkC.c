// Define os endereços dos registradores de hardware do PIC18F1220
#define TRISB_ADDR (volatile unsigned char *)0x0F93
#define LATB_ADDR  (volatile unsigned char *)0x0F8A


void delay_software(void) 
{
    for (volatile long int i = 0; i < 100000; i++);
}

void main() {
    // Configura os pinos RB0, RB1, etc como saída.
    // Em C: *TRISB_ADDR = 0b11111100; (zera os bits 0 e 1)
    *TRISB_ADDR = 0xF8;

    while (1) {
        // Liga LED 1 (RB0) e desliga LED 2 (RB1)
        // Em C: *LATB_ADDR = 0b00000001;
        *LATB_ADDR = 0x01;
        delay_software();

        // Liga LED 2 (RB1) e desliga LED 1 (RB0)
        // Em C: *LATB_ADDR = 0b00000010;
        *LATB_ADDR = 0x02;
        delay_software();
    }
}