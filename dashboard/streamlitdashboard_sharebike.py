# -*- coding: utf-8 -*-
"""StreamlitDashboard_ShareBike.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gAB_vEJ4m9oMe4lwBchzqzyqRJp8JsO6
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
sns.set_theme(style='white')

# Load the dataset
all_df = pd.read_csv("dffix_clean.csv")

# Convert 'date' column to datetime if available
if 'date' in all_df.columns:
    all_df['date'] = pd.to_datetime(all_df['date'])

# Sidebar for filtering
st.sidebar.title("Filters")

# Date filter
if 'date' in all_df.columns:
    min_date = all_df['date'].min()
    max_date = all_df['date'].max()
    selected_date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    if len(selected_date_range) == 2:
        all_df = all_df[(all_df['date'] >= pd.Timestamp(selected_date_range[0])) & (all_df['date'] <= pd.Timestamp(selected_date_range[1]))]

# Weather filter
if 'weathersit_d' in all_df.columns:
    weather_options = all_df['weathersit_d'].unique()
    selected_weather = st.sidebar.multiselect("Select Weather Conditions", weather_options, default=weather_options)
    all_df = all_df[all_df['weathersit_d'].isin(selected_weather)]

# Helper functions
def create_weathermax(df):
    return df.groupby(by="weathersit_d").agg({"cnt_d": "max"}).reset_index()

def create_holidaymax(df):
    return df.groupby(by="holiday_d").agg({"cnt_d": "max"}).reset_index()

def create_reghour(df):
    return df.groupby(by="hr").agg({"registered_h": "mean"}).reset_index()

# Aggregated data
weathersit_max = create_weathermax(all_df)
holiday_max = create_holidaymax(all_df)
reg_hour = create_reghour(all_df)

# Dashboard Title
st.title("Dashboard: Bike Sharing")

# Section: Weather Impact
st.subheader("The Impact of Weather on the Number of Bicycles Borrowed")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Light", value=weathersit_max.loc[weathersit_max['weathersit_d'] == 1, 'cnt_d'].max())
with col2:
    st.metric(label="Cloudy & Mist", value=weathersit_max.loc[weathersit_max['weathersit_d'] == 2, 'cnt_d'].max())
with col3:
    st.metric(label="Light Rain", value=weathersit_max.loc[weathersit_max['weathersit_d'] == 3, 'cnt_d'].max())

fig1 = plt.figure(figsize=(10, 6))
sns.barplot(y="weathersit_d", x="cnt_d", orient="h", data=weathersit_max, palette="Blues")
plt.xlabel("Number of Bicycles Borrowed")
plt.ylabel("Weather Situation")
plt.title("The Impact of Weather on the Number of Bicycles Borrowed")
st.pyplot(fig1)

# Section: Holiday vs Weekdays
st.subheader("Max Volume of Bikes Borrowed Between Weekdays and Holidays")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Weekdays", value=holiday_max.loc[holiday_max['holiday_d'] == 0, 'cnt_d'].max())
with col2:
    st.metric(label="Holidays", value=holiday_max.loc[holiday_max['holiday_d'] == 1, 'cnt_d'].max())

fig2 = plt.figure(figsize=(8, 5))
sns.barplot(x="holiday_d", y="cnt_d", data=holiday_max, palette="coolwarm")
plt.xlabel("Day")
plt.ylabel("Number of Bicycles Borrowed")
plt.title("Max Volume of Bikes Borrowed Between Weekdays and Holidays")
st.pyplot(fig2)

# Section: Registered Users per Hour
st.subheader("Average Registered Bicycle Users Per Hour")

fig3 = plt.figure(figsize=(10, 6))
sns.barplot(x="hr", y="registered_h", data=reg_hour, palette="Greens")
plt.xlabel("Hours")
plt.ylabel("Number of Registered Users")
plt.title("Average Registered Bicycle Users Per Hour")
st.pyplot(fig3)