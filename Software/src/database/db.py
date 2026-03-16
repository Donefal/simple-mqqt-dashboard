import sqlite3
from config import DATABASE

def get_connection():
    return sqlite3.connect(DATABASE)

def create_table_if_not_exists():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data(
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL,
            light_level REAL
        );
        """
    )
    conn.commit()
    conn.close()

def insert_sensor_data(temp, humidity, light):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"INSERT INTO sensor_data (temperature, humidity, light_level) VALUES ({temp}, {humidity}, {light});"
    )

    print("New data sucessfully inserted")
    conn.commit()
    conn.close()

