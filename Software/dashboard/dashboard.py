import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from database.db import get_connection

import streamlit as st
import pandas as pd

st.write('# Simple Sensor Dashboard')
col1, col2, col3 = st.columns(3)

col1.metric(label='Temperature', value="1°C", border=True)
col2.metric(label='Humidity', value=2, border=True)
col3.metric(label='Ligh Level', value=3, border=True)
