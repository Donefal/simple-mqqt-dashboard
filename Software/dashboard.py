import streamlit as st
import pandas as pd
import altair as alt

from streamlit_autorefresh import st_autorefresh
from src.database.db import get_sensor_data, get_led_state, change_led_state
from src.mqtt.publisher import publish_to_mqtt_led

# ----------------------------------------------------------
# Settings
# ----------------------------------------------------------
st_autorefresh(interval=2000, key="RefreshGraph")

df_sensor = get_sensor_data()
led_state = get_led_state()

st.set_page_config(
    page_title="Sensor Dashboard",
    page_icon="📊",
)

# ----------------------------------------------------------
# Upper area
# ----------------------------------------------------------
st.title("Simple Sensor Dashboard")
col1, col2, col3 = st.columns(3)

# Data
latest_temp = list(df_sensor["temperature"].head(2))
delta_temp = round(latest_temp[0] - latest_temp[1], 3)

latest_humd = list(df_sensor["humidity"].head(2))
delta_humd = round(latest_humd[0] - latest_humd[1], 3)

# Metrics
col1.metric(label="Temperature", value=f"{latest_temp[0]}°C", border=True, delta=delta_temp)
col2.metric(label="Humidity", value=f"{latest_humd[0]}%", border=True, delta=delta_humd)

# Buttons
if led_state[0]:
    cont = col3.container(border=True, height="stretch", horizontal_alignment="center", vertical_alignment="center")
    clicked = cont.button("LED State (ON)", type="primary")
else:
    cont = col3.container(border=True, height="stretch", horizontal_alignment="center", vertical_alignment="center")
    clicked = cont.button("LED State (OFF)", type="secondary")

if clicked:
    new_state = not led_state[0]
    publish_to_mqtt_led(new_state)
    change_led_state(new_state)
    st.rerun()
# ----------------------------------------------------------
# Chart Area
# ----------------------------------------------------------

# Line_chart
tab1, tab2, tab3 = st.tabs(["Temperature", "Humidity", "Dataframe"])

tab1.subheader("Temperature (°C)")
chart_temp = alt.Chart(df_sensor).mark_line().encode(
    x=alt.X(
        "timestamp:T",
        axis=alt.Axis(format="%H:%M:%S")
    ),
    y=alt.Y("temperature:Q", scale=alt.Scale(zero=False))
)
tab1.altair_chart(chart_temp)
# tab1.line_chart(df_sensor, x="timestamp", y="temperature", y_label="Temp (°C)", x_label="")

tab2.subheader("Humidity (%)")
chart_humd = alt.Chart(df_sensor).mark_line().encode(
    x=alt.X(
        "timestamp:T",
        axis=alt.Axis(format="%H:%M:%S")
    ),
    y=alt.Y("humidity:Q", scale=alt.Scale(zero=False))
)
tab2.altair_chart(chart_humd)
# tab2.line_chart(df_sensor, x="timestamp", y="humidity", y_label="Humd (%)", x_label="")

tab3.subheader("Dataframe")
tab3.dataframe(df_sensor)

