/*
 * pacman.c
 *
 * Created: 06/05/2023 01:43:26 p. m.
 * Author: KOKAS
 */


#asm
.equ __lcd_port = 0x0B
.equ __lcd_EN = 3
.equ __lcd_RS = 2
.equ __lcd_D4 = 4
.equ __lcd_D5 = 5
.equ __lcd_D6 = 6
.equ __lcd_D7 = 7
#endasm

#include <delay.h>
#include <display.h>
#include <mega328p.h>

#define ADC_VREF_TYPE ((0 << REFS1) | (1 << REFS0) | (0 << ADLAR))

    unsigned int
    read_adc(unsigned char adc_input)
{
    ADMUX = adc_input | ADC_VREF_TYPE;
    delay_us(10);
    ADCSRA |= (1 << ADSC);
    while ((ADCSRA & (1 << ADIF)) == 0);
    ADCSRA |= (1 << ADIF);
    return ADCW;
}

unsigned char pacOpen[] = {
 0x0E,
 0x1D,
 0x1E,
 0x1C,
 0x1E,
 0x1F,
 0x0E,
 0x00};

unsigned char pacClosed[] = {
 0x0E,
 0x1D,
 0x1F,
 0x1F,
 0x1E,
 0x1F,
 0x0E,
 0x00};

unsigned char pacOpenL[] = {
 0x0E,
 0x17,
 0x0F,
 0x07,
 0x0F,
 0x1F,
 0x0E,
 0x00};

unsigned char pacClosedL[] = {
 0x0E,
 0x17,
 0x1F,
 0x0F,
 0x1F,
 0x1F,
 0x0E,
 0x00};

unsigned char closed = 0;
unsigned char open = 1;
unsigned char closedL = 2;
unsigned char openL = 3;
unsigned char line = 0;

signed char i = 0;

void DelayPacMan()
{
    delay_ms(read_adc(0));
}

void main(void)
{
    DIDR0 = (0 << ADC5D) | (0 << ADC4D) | (0 << ADC3D) | (0 << ADC2D) | (0 << ADC1D) | (1 << ADC0D);
    ADMUX = ADC_VREF_TYPE;
    ADCSRA = (1 << ADEN) | (0 << ADSC) | (0 << ADATE) | (0 << ADIF) | (0 << ADIE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
    ADCSRB = (0 << ADTS2) | (0 << ADTS1) | (0 << ADTS0);

    DDRC = 0x02;
    PORTC = 0x02;

    SetupLCD();
    CreateChar(closed, pacClosed);
    CreateChar(open, pacOpen);
    CreateChar(closedL, pacClosedL);
    CreateChar(openL, pacOpenL);

    while (1)
    {

        if (i == 0 && !line)
        {
            MoveCursor(6, 0);
            StringLCD("Hello");
            MoveCursor(4, 1);
            StringLCD("Mr PacMan");
        }

        MoveCursor(i, line);
        CharLCD(PINC.1 ? open : openL);
        DelayPacMan();
        MoveCursor(i, line);
        CharLCD(PINC.1 ? closed : closedL);
        DelayPacMan();
        MoveCursor(i, line);
        CharLCD(' ');

        if (PINC.1)
        {
            i++;
            if (i >= 16)
            {
                i = 0;
                line = !line;
            }
        }
        else
		{
			i--;
			if (i < 0)
			{
				i = 15;
				line = !line;
			}
		}
	}
}