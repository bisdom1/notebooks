import pandas as pd     # pandas for reading csv as dataframe
import streamlit as st  # streamlit app
msfile = st.sidebar.file_uploader("Microseismic data", type=['csv']) # input field for uploading csv files
mmin = st.sidebar.slider("Minumum magnitude: ", -2., 3., 1.)         # slider to select minimum magnitude threshold between -2 and 3
if msfile:              # only run if a file is uploaded
    ms = pd.read_csv(msfile)    # open the file and read as dataframe
    st.line_chart(ms[ms['Moment Magnitude'] > mmin]['Moment Magnitude']) # plot uploaded data, filtered by mmin