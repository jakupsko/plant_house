from machine import ADC, Pin
import utime

class MoistureSensor:
    def __init__(self, manager, adc_pin:int, min_value=None, max_value=None):
        self.misture_sensor = ADC(Pin(adc_pin))
        self.display = manager.display
        self.calibrated_min = min_value
        self.calibrated_max = max_value
            

    def get_average_reading(self, observations:int):
        """Get average moisture reading"""
        readings = []

        for _ in range(observations):
            reading = self.misture_sensor.read_u16()
            readings.append(reading)
            utime.sleep_ms(100)

        return sum(readings) / len(readings)


    def calibrate(self):
        """Calibration reads the ADC value from the sensor 100 times and returns an average"""
        
        iterations = 100

        print('Calibrate sensor for the minimum moisture: air.')
        print('Calibration will start in 10 seconds.')
        for sec in range(10,-1,-1):
            self.display.display_text("Dry Calibration", f"start in {sec} sec")
            utime.sleep(1)

        self.display.display_text(line_1="Keep Dry")
        
        print('Starting minimum calibration')

        min_value = self.get_average_reading(iterations)

        print('Minimum calibration complete')
        self.display.display_text("Dry Calibration", "Done!")
        utime.sleep(2)
        
        print('Calibrate sensor for the maximum moisture: water')
        print('Calibration will start in 10 seconds.')
        
        for sec in range(10,-1,-1):
            self.display.display_text("Wet Calibration", f"start in {sec} sec")
            utime.sleep(1)

        self.display.display_text(line_1="Keep Wet")
        
        print('Starting maximum calibration')

        max_value = self.get_average_reading(iterations)

        print('Maximum calibration complete')
        self.display.display_text("Wet Calibration", "Done!")
        utime.sleep(2)
        
        print('Calibration complete!')
        
        print('min_value = ', round(min_value))
        print('max_value = ', round(max_value))
        self.display.display_text(f"min = {int(round(min_value, -2))}", f"max = {int(round(max_value, -2))}")
        
        return int(round(min_value, -2)), int(round(max_value, -2))
        
    def get_moisture_pct(self):
        """Get moisture percent based on average reading"""
        try:
            percent = ((self.get_average_reading(25) - self.calibrated_min) /
                       (self.calibrated_max - self.calibrated_min)) * 100
        except ZeroDivisionError:
            percent = 0
        
        return int(percent)

if __name__ == '__main__':
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

    
    manager = Manager()
    
    print(manager.config.items)
    
    MIN_VALUE=manager.config.items['moisture_sensor_min']
    MAX_VALUE=manager.config.items['moisture_sensor_max'] 
    
    
    if MIN_VALUE is None or MAX_VALUE is None:
       manager.config.set_moisture_sensor_settings(*manager.moisture_sensor.calibrate())
    else:
        print('No calibration needed')
        
    while True:
        print(f"Moisture {manager.moisture_sensor.get_moisture_pct()}%")
        