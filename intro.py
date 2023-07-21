import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    df=pd.read_csv("datasets/Bakery sales.csv")
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # df["unit_price"]=df.unit_price.str.replace('[^0-9\.-]','',regex=True)
    df["unit_price2"]=df.unit_price.str.replace(",",".")
    df["unit_price2"]=df.unit_price2.str.replace("€"," ")
    df["unit_price2"]=df.unit_price2.str.strip() 
    df["unit_price2"]=df.unit_price2.astype("float")
    df["sales"]=df.Quantity * df.unit_price2
    df.drop('unit_price', axis=1, inplace=True)
    df.drop(df[df.sales==0].index, inplace=True)
    pd.to_datetime(df.date)
    
    
    #to save the clean data into file
    # df.to_csv() 
    return df

st.title("Demo App")

st.subheader("Learn the basic structure")
st.write("Bakery Sales Data")
try:
    df=load_data()

    articles = df.article.unique()
    articles_selection = st.multiselect("choose product", articles, [articles[0], articles[1]])
    articles_selected=df[df["article"].isin(articles_selection)]
    
    # table
    st.write("""### Top 5 Rows""")
    st.write(articles_selected.head())
    
    # bar chart
    st.write("""### Total Sales of Selected Product(s)""")
    bar1 = articles_selected.groupby(['article'])['sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)
    
    #line chart
    st.write("""### Sales over Time""")
    fig, ax = plt.subplots (figsize=(10,6))
    ax.plot(articles_selected['date'], articles_selected['sales'])
    st.pyplot(fig)
    
    # pie chart
    st.write("""### Percentage of selected product(s) sold""")
    pie_data= articles_selected['article'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(7,7))
    ax2.pie(pie_data, labels=pie_data.index, autopct='%.1f%%', shadow=True)
    ax2.axis("equal") # gives equal aspect ratio
    st.write("Note: this is showing pecentage for only the values")
    st.pyplot(fig2)
except ValueError as e:
    st.error("""
        Error:
    """ % e.reason)