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

def HomePage():
    #print dataframe""
    with st.expander("🛢 My database"):
        showdata=st.multiselect("Filter:",df_selection.columns,default=["BusinessName","Location","Region","BusinessType","Investment","ConstructionYear","Rating"])
        st.dataframe(df_selection[showdata],use_container_width=True)

    #compute top analytics
    total_investment=float(df_selection['Investment'].sum())
    investment_mode=float(df_selection['Investment'].mode())
    investment_mean=float(df_selection['Investment'].mean())
    investment_median=float(df_selection['Investment'].median())
    rating=float(df_selection['Rating'].sum())

    #columns
    total1,total2,total3,total4,total5=st.columns(5,gap='large')
    with total1:
        st.info('Total Investment',icon="📌")
        st.metric(label='sum Kshs',value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most Frequently',icon="📌")
        st.metric(label='mode Kshs',value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Investment Averange',icon="📌")
        st.metric(label='mean Kshs',value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Investment Marging',icon="📌")
        st.metric(label='median Kshs',value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings',icon="📌")
        st.metric(label="Rating",value=numerize(rating),help=f"""Total rating: {rating}""")

    st.markdown("""---""")

HomePage()