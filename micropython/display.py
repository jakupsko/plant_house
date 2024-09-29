"""Manages the LCD display and all that is used to control it"""

import utime
from machine import RTC

from lcd import LCD
from rotary_select import Rotary

class Display:
    MENU = ("Show Start Date", "Set Start Date", "Set Moisture", "Calib Moisture")
    
    def __init__(self, manager):
        self.manager = manager
        
        self.lcd = LCD()
        self.rotary = Rotary(dt=12, clk=11, sw=13)
        self.rotary.add_handler(self.handle_rotary_event)        
        
        self.last_button_press = utime.ticks_ms() - 100_000_000
        
        # set default values
        self.temp_moisture_setting = self.manager.config.items['threshold_moisture']
        self.reset_display_settings() # starts off by displaying menu if selector is used         
    
    
    def reset_display_settings(self):
        """Resets display to start next display menu and start at menu choice 1"""
        
        self.position = 0
        self.selector_function = self.display_menu
        
        
    def display_text(self, line_1:str="", line_2:str=""):
        """Display test via external facing call"""
        
        self.lcd.clear()
        self.lcd.lcd_string(line_1, 0)
        self.lcd.lcd_string(line_2, 1)
    
    
    def handle_rotary_event(self, event_type):
        """Handles events after rotary selector input"""
        
        if event_type == self.rotary.ROT_CW:
            self.position += 1
        elif event_type == self.rotary.ROT_CCW:
            self.position -= 1
        elif event_type == self.rotary.SW_RELEASE:
             pass
        elif event_type == self.rotary.SW_PRESS:
            if self.selector_function == self.display_menu:
                if self.position == 0:
                    self.selector_function = self.get_date
                elif self.position == 1:
                    self.selector_function = self.set_date
                elif self.position == 2:
                    self.selector_function = self.set_moisture
                elif self.position == 3:
                    self.selector_function = self.calibrate_moisture_sentor
            else:
                self.manager.config.set_moisture_threshold(self.temp_moisture_setting)
                self.selector_function = self.display_menu
                
            self.position = 0
        
        self.last_button_press = utime.ticks_ms()
        self.selector_function()
        
        
    def display_menu(self):
        """Displays menu on LCD"""
        
        self.position = max(0, min(len(self.MENU) - 1, self.position))
        
        line_1 = f">{self.MENU[self.position]}"
        try:
            line_2 = f" {self.MENU[self.position + 1]}"
        except IndexError:
            line_2 = ""
        
        self.display_text(line_1, line_2)
        
        
    def get_date(self):
        """Display start_date on LCD screen"""
        
        year, month, day = self.manager.config.items['start_date']
        
        line_1 = "Current Start "
        line_2 = f"Date: {year}.{month}.{day}"
        
        self.display_text(line_1, line_2)
        
        
    def set_date(self):
        """Sets new start_date that is equal to today"""
        
        year, month, day, weekday, hour, minute, second, microsecond = RTC().datetime()
        self.manager.config.set_start_date(RTC().datetime())
        
        line_1 = "Start Date Set"
        line_2 = f" To: {year}.{month}.{day}"
        
        self.display_text(line_1, line_2)


    def set_moisture(self):
        """Sets new moisure threshold level"""
        
        self.temp_moisture_setting = self.manager.config.items['threshold_moisture'] + self.position
        
        line_1 = "Set Moisture"
        line_2 = f"{' ' * 3} New: {self.temp_moisture_setting}%"
        
        self.display_text(line_1, line_2)


    def calibrate_moisture_sentor(self):
        """Does new moisture sensor calibration"""
        
        self.manager.config.set_moisture_sensor_settings(*self.manager.moisture_sensor.calibrate())
        self.reset_display_settings()
        
        
if __name__ == '__main__':
    from config import Config
    from moisture import MoistureSensor
            
    class Manager:
         """Goal is to keep track of all instances of classes and share among each other"""
         def __init__(self):
             self.config = Config(self)
             self.display = Display(self)
             self.moisture_sensor = MoistureSensor(adc_pin=27, min_value=self.config.items['moisture_sensor_min'],
                                            max_value=self.config.items['moisture_sensor_max'], manager=self)
    
    
    manager = Manager()
    
    while True:
        if utime.ticks_diff(utime.ticks_ms(), manager.display.last_button_press) >= 2_000:
            # screen saver
            line_1 = f"Screen saver"
            line_2 = f"Display"
            manager.display.display_text(line_1, line_2)
            manager.display.reset_display_settings()

        
        # Add a small delay to avoid busy-waiting
        utime.sleep(1)

