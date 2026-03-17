import paho.mqtt.client as mqtt
import json
from ..database.db import insert_sensor_data

from config import MQTT_BROKER, MQTT_PORT, MQTT_PASSWORD, MQTT_TOPIC, MQTT_USERNAME

def on_connect(client, userdata, flags, rc, properties):
	print(f"connected with result code {rc}")
	client.publish(MQTT_TOPIC, "Hellow from Python")

# Callback when receiving a PUBLISH message on the MQTT
def on_message(client, userdata, msg):
	payload = msg.payload.decode().strip() 
	
	try:
		data = json.loads(payload)
	except json.JSONDecodeError:
		print("Invalid JSON:", payload)
		return
	
	temperature = data.get("temp")
	humidity = data.get("humidity")
	light_level = data.get("light")

	insert_sensor_data(temperature, humidity, light_level)
	print(temperature, humidity, light_level)

def start_mqtt():
	mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	mqttc.on_connect = on_connect
	mqttc.on_message = on_message
	
	mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
	mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
	
	mqttc.subscribe(MQTT_TOPIC)
	mqttc.loop_forever()
    