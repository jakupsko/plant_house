import machine
import ntptime
import utime

from config import Config
from display import Display
from moisture import MoistureSensor
        
class Manager:
     """Goal is to keep track of all instances of classes and share among each other"""
     def __init__(self):
         self.config = Config(self)
         self.display = Display(self)
         self.moisture_sensor = MoistureSensor(adc_pin=27, min_value=self.config.items['moisture_sensor_min'],
                                        max_value=self.config.items['moisture_sensor_max'], manager=self)
         

def main():
     # first, synchronize RTC on startup
    try:
        ntptime.settime()
        print('Time synchronized')
    except Exception as e:
        print('Failed to syncronize time: ', e)

    # create manger and distribute different classes 
    manager = Manager()
    
    manager.display.display_text("Startup Sequence", "in progress...")
    
    # Establish constants
    REST_TIME = 5_000
    NAME = manager.config.items['name']
    MIN_VALUE = manager.config.items['moisture_sensor_min']
    MAX_VALUE = manager.config.items['moisture_sensor_max'] 
    
    print(manager.config.items)

    # If no min and max values for sensor in settings file, then initiate calibration 
    if MIN_VALUE is None or MAX_VALUE is None:
        manager.moisture_sensor.set_moisture_sensor_settings(*sensor.calibrate())
    else:
        print('No moisure sensor calibration needed')
        
    
    while True:
        if utime.ticks_diff(utime.ticks_ms(), manager.display.last_button_press) >= REST_TIME:
            # screen saver
            line_1 = f"{NAME}: Day {manager.config.get_days_grown()}"
            line_2 = f"Moisure: {manager.moisture_sensor.get_moisture_pct()}%"
            manager.display.display_text(line_1, line_2)
            manager.display.reset_display_settings()

        
        # Add a small delay to avoid busy-waiting
        utime.sleep_ms(int(REST_TIME/2))

    
if __name__ == '__main__':
    main()