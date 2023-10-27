import streamlit as st
import time
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Temporal Analysis", page_icon="⌛")

st.title("Temporal Analysis")

# Take data 

data_path = 'Data/'

if 'df' not in st.session_state:
    df = pd.read_csv(data_path + 'BitcoinHeistDataWithMonthAndDate.csv')
else:
    df = st.session_state.df

# Add df to session state
if 'df' not in st.session_state:
    st.session_state.df = df

include_non_ransomware = st.sidebar.checkbox('Include Non-Ransomware', value=False)

if not include_non_ransomware:
    df = df[df['label'] != 'white']

include_ransomware = st.sidebar.checkbox('Include Ransomware', value=True)

if not include_ransomware:
    df = df[df['label'] == 'white']

if not include_non_ransomware and not include_ransomware:
    st.warning('Both options unchecked. No data to show.')

if include_ransomware or include_non_ransomware:
    if include_ransomware:
        choose_all_ransomware = st.sidebar.checkbox('All Ransomware', value=True)

        if not choose_all_ransomware:
            ransomware = st.sidebar.multiselect('Select Ransomware', df['label'].unique(), default=['princetonCerber'])
            df = df[df['label'].isin(ransomware)]

    # Choose year wise, monthwise or daywise from dropdown
    choose_time = st.sidebar.selectbox('Choose Investigation Mode', ['Year', 'Month', 'Day for a Given Month', 'Day for a Given Month and Year'])

    if choose_time == 'Year':
        year_dist = df['year'].value_counts()
        year_dist = year_dist.sort_index()
        fig = go.Figure(data=[go.Bar(x=year_dist.index, y=year_dist.values)])
        fig.update_layout(title_text='Year Distribution')
        st.plotly_chart(fig)
    elif choose_time == 'Month':
        month_dist = df['month'].value_counts()
        month_dist = month_dist.sort_index()
        fig = go.Figure(data=[go.Bar(x=month_dist.index, y=month_dist.values)])
        fig.update_layout(title_text='Month Distribution')
        # Change x-axis labels
        fig.update_xaxes(ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                                'Nov', 'Dec'])
        st.plotly_chart(fig)
    elif choose_time == 'Day for a Given Month':
        st.sidebar.write('Choose a month')
        # Month to number mapping
        mapping = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6, 
                'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec':12}
        month = st.sidebar.selectbox('Select Month', mapping.keys())
        month_df = df[df['month'] == mapping[month]]
        day_dist = month_df['date'].value_counts()
        day_dist = day_dist.sort_index()
        fig = go.Figure(data=[go.Bar(x=day_dist.index, y=day_dist.values)])
        fig.update_layout(title_text=f'Day Distribution for {month}')
        st.plotly_chart(fig)
    else:
        st.sidebar.write('Choose a month')
        # Month to number mapping
        mapping = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6, 
                'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec':12}
        month = st.sidebar.selectbox('Select Month', mapping.keys())
        st.sidebar.write('Choose a year')
        year = st.sidebar.selectbox('Select Year', df['year'].unique())
        month_df = df[df['month'] == mapping[month]]
        month_df = month_df[month_df['year'] == year]
        day_dist = month_df['date'].value_counts()
        day_dist = day_dist.sort_index()
        fig = go.Figure(data=[go.Bar(x=day_dist.index, y=day_dist.values)])
        fig.update_layout(title_text=f'Day Distribution for {month}')
        st.plotly_chart(fig)