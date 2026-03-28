import sqlite3
import pandas as pd

from config import DATABASE

def get_connection():
    return sqlite3.connect(DATABASE)

def create_table_if_not_exists():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data(
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS led_data(
            id INTEGER PRIMARY KEY,
            state BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )

    cur.execute(
        """
        SELECT 1 FROM led_data;
        """
    )

    if not cur.fetchone():
        cur.execute(
            """
            INSERT INTO led_data VALUES (0, 0);
            """
        )
        print("New LED Data created")
    else:
        print("LED Data ready to be used")

    conn.commit()
    conn.close()

# ----------------------------------------------------------
# SENSOR STUFF
# ----------------------------------------------------------

def insert_sensor_data(temp, humidity):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?);",
        (temp, humidity)
    )

    print("New sensor data sucessfully inserted")
    conn.commit()
    conn.close()

def get_sensor_data():
    conn = get_connection()

    sql_query = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10"

    df = pd.read_sql_query(sql=sql_query, con=conn)
    return df

# ----------------------------------------------------------
# LED STUFF
# ----------------------------------------------------------
def change_led_state(led_state):
    conn = get_connection()
    cur = conn.cursor()

    # Change LED State
    cur.execute(
        """
        UPDATE led_data
        SET state = (?)
        WHERE id = 0;
        """, 
        (led_state,)
    )

    print("LED data sucessfully changed")
    conn.commit()
    conn.close()

def get_led_state():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT state FROM led_data WHERE id = 0;"
    )

    state = cur.fetchone()
    if state:
        return state
    else:
        print("ERROR on getting LED State")