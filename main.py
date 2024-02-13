import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu

from mysql_con import *

st.set_page_config("Business Amalytics Dashboard", page_icon="", layout="wide")
st.subheader("Business Analystics Dashboard")

