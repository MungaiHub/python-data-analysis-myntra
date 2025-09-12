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

 # graphs
def graphs():
    #total_price=int(df_selection["price"]).sum()
    #averangerating=int(round(df_selection["ratings"]).mean(),2)

    #simple line graph
    price_by_brand_name=(
        df_selection.groupby(by=["brand_name"]).count()[["price"]].sort_values(by="price")
    )
    fig_price=px.bar(
        price_by_brand_name,
        x="price",
        y=price_by_brand_name.index,
        orientation="h",
        title="<b>price by brand name</b>",
        color_discrete_sequence=["#0083b8"]*len(price_by_brand_name),
        template="plotly_white",
    )
    
    fig_price.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
    )


#simple line graph
    price_by_pants_description=(
        df_selection.groupby(by=["pants_description"]).count()[["price"]]
    )
    fig_pants_description=px.line(
        price_by_pants_description,
        x=price_by_pants_description.index,
        y="price",
        orientation="v",
        title="<b>price by pants description</b>",
        color_discrete_sequence=["#0083b8"]*len(price_by_pants_description),
        template="plotly_white",
    )
    fig_pants_description.update_layout(
    xaxis=(dict(tickmode="linear")),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
    )

    left,right=st.columns(2)
    left.plotly_chart(fig_pants_description, use_container_width=True)
    right.plotly_chart(fig_price, use_container_width=True)

Home() 
graphs()
    