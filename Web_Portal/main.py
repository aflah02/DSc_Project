import streamlit as st
import os
import pandas as pd

st.set_page_config(
    page_title="Main",
    page_icon="🎯",
)

data_path = 'Data/'

def main():
    st.title("Analyzing Bitcoin Heist Data")

    if 'df' not in st.session_state:
        df = pd.read_csv(data_path + 'BitcoinHeistDataWithMonthAndDate.csv')
    else:
        df = st.session_state.df
    
if __name__ == "__main__":
    main()