import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query  import *

st.set_page_config(page_title="Dashboard",layout="wide")
st.subheader("Myntra Sales Descriptive Analytics")
st.markdown('##')




result=view_all_data()
columns = ["id","brand_name", "pants_description", "price", "MRP", "discount_percent", "ratings", "number_of_ratings"]
df = pd.DataFrame(result, columns=columns)
st.dataframe(df)