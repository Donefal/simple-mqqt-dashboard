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

def change_led_data(led_state):
    conn = get_connection()
    cur = conn.cursor()

    # FIXME: STILL EROR ON THIS EXECUTE FUNCTION
    cur.execute(
        """
        UPDATE led_data
        SET state = 1
        WHERE id = 0;
        """
    )

    print("LED sucessfully changed")
    conn.commit()
    conn.close()

