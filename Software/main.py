from src.mqtt.subscriber import start_mqtt
from src.database.db import create_table_if_not_exists

if __name__ == "__main__":
    create_table_if_not_exists()
    start_mqtt()