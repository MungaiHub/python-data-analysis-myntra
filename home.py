import streamlit as st
import pandas as pandas
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize

st.set_page_config(page_title="Dashboard",layout="wide")
st.subheader("Myntra Sales Descriptive Analytics")