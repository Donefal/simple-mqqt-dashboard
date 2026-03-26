from src.mqtt.subscriber import start_mqtt_subscriber
from src.mqtt.publisher import publish_init
from src.database.db import create_table_if_not_exists

if __name__ == "__main__":
    create_table_if_not_exists()
    start_mqtt_subscriber()
    publish_init()