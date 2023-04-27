import time
from hcsr04 import HCSR04
from umqttsimple import MQTTClient
import ubinascii
from machine import Pin, unique_id
import micropython
import network
import json
import esp
import ntptime
esp.osdebug(None)
import gc
gc.collect()

# Water Vars
max_water_level = 9.46
critical_water_level_percent = 25
min_water_level = 0

# Sensor init
print("Init Sensor!")
trig_port = 1
echo_port = 2
sensor = HCSR04(trigger_pin=trig_port, echo_pin=echo_port)

# Init LED
led = Pin(4, Pin.OUT)

# Network init
print("Init Network!")

ssid = ''
password = ''
mqtt_server_host = ''
mqtt_server_port = 1883
mqtt_user = ''
mqtt_password = ''
client_id = ubinascii.hexlify(unique_id())
topic_sub = b'ovm_lf7_test_topic'
topic_pub = b'ovm_lf7_test_topic'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while not station.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected to WiFi!")

print(station.ifconfig())


# Init Time
print("Init Time!")
trys = 10

ntptime.host = "1.europe.pool.ntp.org"
for i in range(1, 10):
  try:
    print("Local time before synchronization：%s" %str(time.localtime()))
    #make sure to have internet connection
    ntptime.settime()
    print("Local time after synchronization：%s" %str(time.localtime()))
    break;
  except Exception as e:
    print(".", end="")
    time.sleep(1)
