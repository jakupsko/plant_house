import ujson
import utime
from machine import RTC

class Config():
        def __init__(self, manager):
            self.manager = manager
            with open('settings.json', 'r') as f:
                self.items = ujson.load(f)
        
        def save_settings(self):
            """Saves settings back to json file"""
            
            with open('settings.json', 'w') as f:
                ujson.dump(self.items, f)
                
        
        def get_items(self):
            """For ease of listing all items being kept track in settings.json"""
            
            return self.items
        
        
        def set_start_date(self, new_date:tuple):
            """Sets new start_date"""
            
            self.items['start_date'] = new_date[0:3]
            self.save_settings()
            
        
        def set_moisture_threshold(self, new_level):
            """Sets new moisure_threshold"""
            
            self.items['threshold_moisture'] = new_level
            self.save_settings()
            
            
        def set_moisture_sensor_settings(self, min_value:int, max_value:int):
            """Set new moisure sensor min and max values, and saves to json file"""
            
            self.items['moisture_sensor_min'] = min_value
            self.items['moisture_sensor_max'] = max_value
            self.save_settings()
            

        def get_days_grown(self):        
            """Returns number of days since start_date"""
            
            time1 = utime.mktime((list(self.items['start_date']) + [1] * 8)[:8])
            time2 = utime.mktime(RTC().datetime())
            
            return (time2 - time1) // (24 * 60 * 60)
        
        
        
if __name__ == '__main__':
    s = Config()
    print(s.items)
    print(s.get_days_grown())