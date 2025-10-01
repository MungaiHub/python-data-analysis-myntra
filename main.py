import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import plotly.express as px
import time
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

#page behavour
st.set_page_config(page_title="Descriptive Analytics",page_icon="📈",layout="wide")

#remove default theme
theme_plotly=None

#style
with open ('style.css') as f:
    st.markdown(f"<style>{f.read()}</style", unsafe_allow_html=True)

#load excel file
df=pd.read_excel('data/business_dataset.xlsx',sheet_name='Sheet1')

#switcher
st.sidebar.header("Please Filter Here:")
region=st.sidebar.multiselect("Select the Region:",options=df["Region"].unique(),default=df["Region"].unique())
location=st.sidebar.multiselect("Select the Location:",options=df["Location"].unique(),default=df["Location"].unique())
Business_type=st.sidebar.multiselect("Select the Business Type:",options=df["BusinessType"].unique(),default=df["BusinessType"].unique())

df_selection=df.query(
    "Region == @region & Location==@location & BusinessType == @Business_type"
)
  

