import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load data
bike_share_df = pd.read_csv('merged_data.csv')

def create_rent_df(df):
    rent_df = df.groupby(by='dteday').agg({
        'cnt_day': 'sum'
    }).reset_index()
    return rent_df

def create_casual_df(df):
    casual_df = df.groupby(by='dteday').agg({
        'casual_day': 'sum'
    }).reset_index()
    return casual_df

def create_registered_df(df):
    registered_df = df.groupby(by='dteday').agg({
        'registered_day': 'sum'
    }).reset_index()
    return registered_df

def create_season_df(df):
    season_df = df.groupby(by='season_day')[['registered_day', 'casual_day']].sum().reset_index()
    return season_df

def create_monthly_df(df):
    monthly_df = df.groupby(by='mnth_day').agg({
        'cnt_day': 'sum'
    })
    sorted_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    monthly_df = monthly_df.reindex(sorted_months, fill_value=0)
    return monthly_df

def create_weathersit_df(df):
    weathersit_df = df.groupby(by='weathersit_day').agg({
        'cnt_day': 'sum'
    })
    return weathersit_df

def create_hr_df(df):
    hr_df = df.groupby(by='dteday').agg({
        'cnt_day': 'sum'
    }).reset_index()
    return hr_df

#filter
min_date = pd.to_datetime(bike_share_df["dteday"]).dt.date.min()
max_date = pd.to_datetime(bike_share_df["dteday"]).dt.date.max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = bike_share_df[(bike_share_df["dteday"] >= str(start_date)) & 
                (bike_share_df["dteday"] <= str(end_date))]

rent_df = create_rent_df(main_df)
casual_df = create_casual_df(main_df)
registered_df = create_registered_df(main_df)
season_df = create_season_df(main_df)
monthly_df = create_monthly_df(main_df)
weathersit_df = create_weathersit_df(main_df)
hr_df = create_hr_df(main_df)


st.write(
    """
    # 🚲Bike Sharing Dashboard
    Welcome!
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    casual = casual_df['casual_day'].sum()
    st.metric('Casual Cust', value= casual)

with col2:
    registered = registered_df['registered_day'].sum()
    st.metric('Registered Cust', value= registered)
 
with col3:
    rent = rent_df['cnt_day'].sum()
    st.metric('Total', value= rent)

#grafik bulan
st.subheader("Monthly Rental Report")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_df.index,
    monthly_df["cnt_day"],
    marker='o', 
    linewidth=2,
    color="red"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#jam
st.subheader("Hourly Rental Report")
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='hr',
    y='cnt_day',
    data=bike_share_df,
    color='blue',
    ci=None,
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#season
st.subheader("Seasonal Rental Report")
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season_day',
    y='cnt_day',
    data=bike_share_df,
    palette='pastel',
    ci=None,
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#weather
st.subheader("Weather Rental Report")
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='weathersit_day',
    y='cnt_day',
    data=bike_share_df,
    palette='rocket',
    ci=None,
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)
