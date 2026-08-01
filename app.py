import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Life-OS",
    page_icon="🧠",
    layout="wide"
)

st.title("Your Personal Life-OS")

st.caption("AI Powered Digital Wellbeing Dashboard")

df=pd.read_csv("screentime.csv")

st.write(df.head()) #preview of first 5 rows

st.sidebar.header("Controls")

dates=sorted(df["Date"].unique())
selected_day=st.sidebar.selectbox(
    "Choose date",
    dates
)

goal=st.sidebar.slider(
    "Daily Goal (in minutes)",
    20 ,#min value
    600, #max value
    240, #default value
    step=10
)
today_df = df[df["Date"] == selected_day] #stores the row which meet the condition and return True

#calculates key performance indicator

total_minutes= today_df["Minutes_Used"].sum() #total screen time
top_app=(today_df
         .groupby("App_Name")["Minutes_Used"]
         .sum()
         .idxmax()
         )

delta = goal - total_minutes
