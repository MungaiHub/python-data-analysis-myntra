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
from datetime import datetime

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
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode()[0])
    investment_mean = float(df_selection['Investment'].mean())
    investment_median = float(df_selection['Investment'].median())
    rating = float(df_selection['Rating'].sum())


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

def Graphs ():
    total_investments=int(df_selection["Investment"].sum())
    averange_rating=round(df_selection["Rating"].mean(),1)
    star_rating="star:" * int(round(averange_rating, 0))
    averange_investment=round(df_selection["Investment"].mean(),2) 
     
     #simple bar graph
    investment_by_businessType=(
         df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
     )
    fig_investment=px.bar(
        investment_by_businessType,
        x="Investment",
        y=investment_by_businessType.index,
        orientation="h",
        title="Investment by Business Type",
        color_discrete_sequence=["#0083B8"] * len(investment_by_businessType),
        template="plotly_white"
    )
    fig_investment.update_layout(
       plot_bgcolor="rgba(0,0,0,0)",
       xaxis=(dict(showgrid=False,tickformat="~s",dtick=1000000,automargin=True)) 
     )
    
         #simple line graph
    investment_by_region=(
         df_selection.groupby(by=["Region"]).count()[["Investment"]]
     )
    fig_region=px.line(
        investment_by_region,
        x=investment_by_region.index,
        y="Investment",
        orientation="v",
        title="Investment by Region",
        color_discrete_sequence=["#0083B8"] * len(investment_by_region),
        template="plotly_white"
    )
    fig_investment.update_layout(
       xaxis=dict(tickmode="linear"),
       plot_bgcolor="rgba(0,0,0,0)",
       yaxis=(dict(showgrid=False)) 
     )
    
    left_column,right_column, center=st.columns(3)
    left_column.plotly_chart(fig_region, use_container_width=True)
    right_column.plotly_chart(fig_investment,use_container_width=True)

    #pie chart
    with center:
        fig=px.pie(df_selection,values='Rating', names='Region',title='Regions by Ratings')
        fig.update_layout(legend_title="Regions", legend_y=0.9)
        fig.update_traces(textinfo='percent+label',textposition='inside')
        st.plotly_chart(fig,use_container_width=True, theme=theme_plotly)

#progress bar
def ProgressBar():
    st.markdown("""<style>.stprogress > div > div > div > div {background-image:linear-gradient(to right, #99ff99, #FFFF00)}</style""",unsafe_allow_html=True)
    target=2000000000
    current=df_selection["Investment"].sum()
    percent=round((current/target*100))
    my_bar=st.progress(0)

    if percent>100:
        st.subheader("Target 100 complited")

    else:
        st.write("You have", percent, " % " ," of ", (format(target, ',d')), "Kshs.")
        for percent_complete in range(percent):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text="Target percentage")

def sidebar():
    with st.sidebar:
        selected=option_menu(
            menu_title="Menu",
            options=["Home", "Progress"],
            icons=["house","eye"],
            menu_icon="cast", #option
            default_index=0 #option
            )

    if selected == "Home":
        try:
            HomePage()
            Graphs()
        except:
            st.Warning("one or more options are mandatory! ")
    
    if selected=="Progress":
        try:
            ProgressBar()
            Graphs()

        except:
             st.Warning("one or more options are mandatory! ")
    
        
sidebar()




# Footer
footer = f"""
<style>
.footer {{
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #111; /* dark background */
    color: #ddd; /* light gray text */
    text-align: center;
    padding: 12px;
    font-size: 14px;
    border-top: 1px solid #333;
}}
.footer a {{
    color: #FF4B4B; /* Streamlit accent red */
    text-decoration: none;
    font-weight: bold;
}}
.footer a:hover {{
    text-decoration: underline;
}}
</style>
<div class="footer">
    Developed by <a href="https://github.com/mungaihub" target="_blank">MungaiHub</a> | © {datetime.now().year} <br>
    Contact: <a href="mailto:amosmungai085@gmail.com">amosmungai085@gmail.com</a>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
