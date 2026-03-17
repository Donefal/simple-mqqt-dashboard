import streamlit as st
import pandas as pd
from src.database.db import get_connection

st.set_page_config(
    page_title="Sensor Dashboard",
    page_icon="📊",
)

st.sidebar.success("Also see about the project!")

st.write('# Simple Sensor Dashboard')
col1, col2, col3 = st.columns(3)

col1.metric(label='Temperature', value="1°C", border=True)
col2.metric(label='Humidity', value=2, border=True)
col3.metric(label='Ligh Level', value=3, border=True)
