""" Controls 16x2 LCD via I2C """

from machine import I2C, Pin
import utime

class LCD:    
    # LCD Address
    I2C_ADDR = 0x27
    LCD_WIDTH = 16 # number of characters per line

    # LCD Commands
    LCD_CHR = 1  # Mode - Sending data
    LCD_CMD = 0  # Mode - Sending command

    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

    LCD_BACKLIGHT = 0x08  # On
    ENABLE = 0b00000100  # Enable bit, used to toggle the enable pin

    # Timing constants - pulse and delay times for toggling the enable pin
    E_PULSE = 0.001 
    E_DELAY = 0.0005

    I2C_ID = 0
    SDA_PIN = 8
    SCL_PIN = 9

    def __init__(self):
        # Initialize I2C
        self.i2c = I2C(id=self.I2C_ID, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN), freq=400000)
        self._lcd_init()

    def _lcd_byte(self, bits, mode):
        """ Send byte to data pins """
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.i2c.writeto(self.I2C_ADDR, bytearray([bits_high]))
        self._lcd_toggle_enable(bits_high)

        self.i2c.writeto(self.I2C_ADDR, bytearray([bits_low]))
        self._lcd_toggle_enable(bits_low)

    def _lcd_toggle_enable(self, bits):
        """ Toggle enable pin on LCD """
        utime.sleep(self.E_DELAY)
        self.i2c.writeto(self.I2C_ADDR, bytearray([bits | self.ENABLE]))
        utime.sleep(self.E_PULSE)
        self.i2c.writeto(self.I2C_ADDR, bytearray([bits & ~self.ENABLE]))
        utime.sleep(self.E_DELAY)

    def _lcd_init(self):
        """ Initialize display """
        self._lcd_byte(0x33, self.LCD_CMD) # command to initialize LCD in 8-bit mode
        self._lcd_byte(0x32, self.LCD_CMD) # command to switch LCD from 8-bit to 4-bit mode
        self._lcd_byte(0x06, self.LCD_CMD) # command to set entry mode. It sets the cursor to move to the right and ensures the display is not shifted
        self._lcd_byte(0x0C, self.LCD_CMD) # command to turn on the display and turn off the cursor. Ensures display is visible without blinking cursor
        self._lcd_byte(0x28, self.LCD_CMD) # command that sets the LCD to 4-bit mode, 2-line display, and 5x8 dot format
        self._lcd_byte(0x01, self.LCD_CMD) # command that clears any existing text on the LCD and moves the cursor to the home position 
        utime.sleep(self.E_DELAY)

    def clear(self):
        self._lcd_byte(0x01, self.LCD_CMD) # command that clears any existing text on the LCD and moves the cursor to the home position

    def lcd_string(self, message:str, line:int):
        """ Send string to display """
        message = message + " " * self.LCD_WIDTH
        message = message[0:self.LCD_WIDTH]
        
        if line % 2 == 0:
            line_adress = self.LCD_LINE_1
        else:
            line_adress = self.LCD_LINE_2

        self._lcd_byte(line_adress, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self._lcd_byte(ord(message[i]), self.LCD_CHR)

if __name__ == '__main__':
    # Initialize the LCD
    lcd = LCD()

    # # Display message
    lcd.lcd_string("Hello World!", 0)
    lcd.lcd_string("Boom", 1)
