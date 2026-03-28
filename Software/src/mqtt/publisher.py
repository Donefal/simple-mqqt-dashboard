import paho.mqtt.client as mqtt
import json
import time

from config import MQTT_BROKER, MQTT_PORT, MQTT_PASSWORD, MQTT_USERNAME, MQTT_TOPIC_LED
from src.database.db import get_led_state

# FIXME: This is somehow not working at dashboard.py
def publish_to_mqtt_led(led_state):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	
    mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqttc.loop_start()

    data = json.dumps({"led_con": led_state})
    
    msg_info = mqttc.publish(MQTT_TOPIC_LED, data, qos=1)
    msg_info.wait_for_publish()

    mqttc.disconnect()
    mqttc.loop_stop()
    print("LED data sucessfully published")

def publish_init():
    led_state = get_led_state()
    publish_to_mqtt_led(led_state)