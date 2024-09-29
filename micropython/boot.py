"""Automatically runs this file before executing main.py"""

import network
from secrets import WIFI_SSID, WIFI_PASS

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    
    while not wlan.isconnected():
        pass
    
    print("Conected to Wi-Fi")
    print("Network config:", wlan.ifconfig())
    
connect_to_wifi()