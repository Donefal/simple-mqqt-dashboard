import paho.mqtt.client as mqtt
import json
from ..database.db import insert_sensor_data

from config import MQTT_BROKER, MQTT_PORT, MQTT_PASSWORD, MQTT_USERNAME, MQTT_TOPIC_SENSOR

def on_connect(client, userdata, flags, rc, properties):
	print(f"connected with result code: {rc}")
	client.publish(MQTT_TOPIC_SENSOR, "Hellow from Python")

# Callback when receiving a PUBLISH message on the MQTT
def on_message(client, userdata, msg):
	payload = msg.payload.decode().strip() 
	
	try:
		data = json.loads(payload)
	except json.JSONDecodeError:
		print("Invalid JSON:", payload)
		return
	
	if msg.topic == MQTT_TOPIC_SENSOR:
		temperature = data.get("temperature")
		humidity = data.get("humidity")

		insert_sensor_data(temperature, humidity)
		print(temperature, humidity)
	else:
		print("Invalid MQTT Topic to subscribe")
		

def start_mqtt_subscriber():
	mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	mqttc.on_connect = on_connect
	mqttc.on_message = on_message
	mqttc.on_disconnect = start_mqtt_subscriber
	
	mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
	mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
	
	mqttc.subscribe(MQTT_TOPIC_SENSOR)
	mqttc.loop_forever()
    