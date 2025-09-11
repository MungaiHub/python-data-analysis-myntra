import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query  import *

st.set_page_config(page_title="Dashboard",layout="wide")
st.subheader("Myntra Sales Descriptive Analytics")
st.markdown('##')



#fetch data
result=view_all_data()
columns = ["id","brand_name", "pants_description", "price", "MRP", "discount_percent", "ratings", "number_of_ratings"]
df = pd.DataFrame(result, columns=columns)

#sidebar
st.sidebar.image("data/logo.jpg", caption="sales analytics")

#switcher
st.sidebar.header("please filter")
brand_name=st.sidebar.multiselect(
    "select brand name",
    options=df["brand_name"].unique(),
    default=df["brand_name"].unique(),
)
price=st.sidebar.multiselect(
    "select price",
    options=df["price"].unique(),
    default=df["price"].unique(),
)
number_of_ratings=st.sidebar.multiselect(
    "select number of ratings",
    options=df["number_of_ratings"].unique(),
    default=df["number_of_ratings"].unique(),
)

df_selection=df.query(
    "brand_name==@brand_name & price==@price & number_of_ratings==@number_of_ratings"
)

def Home():
    with st.expander("Tabular"):
        showData=st.multiselect('Filter: ',df_selection.columns, default=[])
        st.write(df_selection[showData])

#compute top analytics
total_price=df_selection["price"].sum()
mode_price=df_selection["price"].mode()
mean_price=df_selection["price"].mean()
median_price=df_selection["price"].median()
rating=df_selection["ratings"].sum()

total1,total2,total3,total4,total5=st.columns(5, gap='large')
with total1:
    st.info('Total price')
    st.metric(label="sum Kshs", value=f"{total_price:,.0f}")

with total2:
    st.info('most frequent')
    mode_price = df_selection["price"].mode()[0] 
    st.metric(label="mode Kshs", value=f"{mode_price:,.0f}")

with total3:
    st.info('Averange')
    st.metric(label="averange Kshs", value=f"{mean_price:,.0f}")

with total4:
    st.info('Central Earnings')
    st.metric(label="median Kshs", value=f"{median_price:,.0f}")

with total5:
    st.info('Ratings')
    st.metric(label="Rating", value=numerize(rating), help=f"""Total Rating: {rating}""")

st.markdown("""---""")
Home()