import streamlit as st
import pandas as pd

from src.database.db import get_sensor_data, get_led_state, change_led_state
from src.mqtt.publisher import publish_to_mqtt_led

# ----------------------------------------------------------
# Settings
# ----------------------------------------------------------

df_sensor = get_sensor_data()
led_state = get_led_state()

st.write(led_state[0])

st.set_page_config(
    page_title="Sensor Dashboard",
    page_icon="📊",
)

st.sidebar.success("Also see about the project!")

# ----------------------------------------------------------
# Upper area
# ----------------------------------------------------------
st.title("Simple Sensor Dashboard")
col1, col2 = st.columns(2)

# Data
latest_temp = list(df_sensor["temperature"].head(2))
delta_temp = round(latest_temp[0] - latest_temp[1], 3)

latest_humd = list(df_sensor["humidity"].head(2))
delta_humd = round(latest_humd[0] - latest_humd[1], 3)

# Metrics
col1.metric(label="Temperature", value=f"{latest_temp[0]}°C", border=True, delta=delta_temp)
col2.metric(label="Humidity", value=f"{latest_humd[0]}%", border=True, delta=delta_humd)

# Buttons
col_button1, col_button2 = st.columns(2)

if led_state[0]:
    clicked = col_button1.button("LED State (ON)", type="primary")
else:
    clicked = col_button1.button("LED State (OFF)", type="secondary")

# TODO: Try to test the publish_to_mqtt_led first using python terminal
if clicked:
    new_state = not led_state[0]
    # publish_to_mqtt_led(new_state)
    change_led_state(new_state)
    st.rerun()

clicked2 = col_button2.button("Refresh Pages", type="secondary")
if clicked2: st.rerun()

st.space("small")
# ----------------------------------------------------------
# Chart Area
# ----------------------------------------------------------

# Line_chart
tab1, tab2, tab3 = st.tabs(["Temperature", "Humidity", "Dataframe"])

tab1.subheader("Temperature (°C)")
tab1.line_chart(df_sensor, x="timestamp", y="temperature", y_label="Temp (°C)", x_label="")

tab2.subheader("Humidity (%)")
tab2.line_chart(df_sensor, x="timestamp", y="humidity", y_label="Humd (%)", x_label="")

tab3.subheader("Dataframe")
tab3.dataframe(df_sensor)

