# Sensor Part
def get_water_level():
  global max_water_level, sensor, min_water_level
  distance = sensor.distance_cm()
  if distance < min_water_level:
    distance = min_water_level
  elif distance > max_water_level:
    distance = max_water_level
  return distance

def critical_water_level(distance):
  global max_water_level, critical_water_level_percent
  water_level = max_water_level - distance
  return water_level < max_water_level * (critical_water_level_percent/100)

def build_msg(distance):
  data = {
    'timestamp': time.time(),
    'distance': distance,
   }
  json_sting = json.dumps(data)
  encode_data = json_sting.encode('utf-8')
  print(encode_data)
  return encode_data

# MQTT Part
def sub_cb(topic, msg):
  print((topic, msg))
  if topic == topic_sub and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server_host, topic_sub, mqtt_user, mqtt_password, mqtt_server_port
  client = MQTTClient(client_id, mqtt_server_host, port=mqtt_server_port, user=mqtt_user, password=mqtt_password, keepalive=60)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server_host, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

# Init MQTT

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()


# Loop
while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      print(time.time())
      # Get Data
      distance = get_water_level()
      # Led
      if critical_water_level(distance):
        led.on()
      else:
        led.off()
      # Build msg
      msg = build_msg(distance)
      # Publish
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()
