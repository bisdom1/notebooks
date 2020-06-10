#!/usr/bin/env python
# coding: utf-8

# Example of how to quickly turn a script into an app using python package streamlit (https://streamlit.io/)
# To run:
# 1. Install streamlit package (start Anaconda prompt, type 'pip install streamlit')
# 2. In Anaconda prompt, type 'python run C:/path/to/script/app.py'
# 3. App will start in browser (use chrome or edge, not internet explorer)

import numpy as np  # array operations
import pandas as pd # dataframe operations
import plotly.express as px # plotting dataframes
import streamlit as st # to make the app
import plotly.graph_objects as go

# Create a sidebar with 3 upload file requests
msfile = st.sidebar.file_uploader("Microseismic data", type=['csv'])
wellfile = st.sidebar.file_uploader("Well location data", type=['csv'])
volfile = st.sidebar.file_uploader("Well volume data", type=['csv'])
mmin = st.sidebar.slider("Minumum magnitude: ", 0., 3., 1.)

# Load the data
if msfile:
    microseismic = pd.read_csv(msfile)
    st.subheader(":white_check_mark: Loaded microseismic data")
else:
    st.subheader(":arrow_right: Load microseismic data")

if wellfile:
    well_locations = pd.read_csv(wellfile)
    st.subheader(":white_check_mark: Loaded well locations")
else:
    st.subheader(":arrow_right: Load well locations")

if volfile:
    well_volumes = pd.read_csv(volfile)
    st.subheader(":white_check_mark: Loaded well rates")
else:
    st.subheader(":arrow_right: Load well rates")

# If all data is loaded, process and merge the data
if msfile and wellfile and volfile:
    # Process microseismic
    microseismic.index = pd.to_datetime(microseismic['Date'])
    microseismic = microseismic[microseismic['Moment Magnitude'] > mmin]
    microseismic['monthyear'] = microseismic.to_period('M').index.strftime("%Y-%m-%d")
    microseismic['Events'] = 1 # add a field for storing event counts
    ms_fieldwide = microseismic[['Events']].resample('M').count() # resample microseismic to events per month
    ms_fieldwide.index = ms_fieldwide.to_period('M').index
    
    # Process well volumes
    well_volumes['START_DATE'] = pd.to_datetime(well_volumes['START_DATE'])
    well_volumes['INJECTED'] = well_volumes['STEAM_INJECTION'] + well_volumes['WATER_INJECTION']
    well_volumes['PRODUCED'] = well_volumes[['OIL','WATER']].sum(axis=1)
    well_volumes['TOTAL'] = -well_volumes['INJECTED'] + well_volumes['PRODUCED']
    well_volumes[['prefix','w_id']] = well_volumes['HOLE_NAME'].str.split('-',expand=True)

    # Process well locations
    well_locations['w_id'] = well_locations['Name'].str.replace('PGKYP','')
    well_locations.index = well_locations['w_id']

    # Aggregate volumes for entire field
    fieldwide_volumes = well_volumes.groupby(by='START_DATE').sum()
    fieldwide_volumes['date'] = fieldwide_volumes.index
    fieldwide_volumes.index = fieldwide_volumes.to_period('M').index

    # Volumes per well
    volume_per_well = well_volumes.pivot_table(index='START_DATE',columns='w_id',values='TOTAL')
    volume_per_well.index = volume_per_well.index.to_period('M') 
    volume_per_well.fillna(0,inplace=True)

    # Combine volumes with well location data
    summed_volumes = well_volumes.groupby(by='w_id').sum()
    wells = pd.merge(well_locations, summed_volumes, left_index=True, right_index=True)    

    # Add microseismic summary to combined dataset
    merged_final = pd.merge(ms_fieldwide, volume_per_well, left_index=True, right_index=True)

    # Get correlations
    corr_per_well = merged_final.corr()
    corr_per_well['labels'] = corr_per_well.columns # some cleaning up/formatting for plotting 
    corr_per_well[corr_per_well == 1] = np.nan

    wells_final = pd.merge(wells, corr_per_well[['Events']], left_index=True, right_index=True)
    wells_final = wells_final.rename(columns = {'Events':'Correlation'}) # rename a column name

    # Create some figures
    fig = px.scatter(microseismic, x='Date', y='Moment Magnitude',color='Depth_SS [m]',opacity=.5, title='Microseismic events')
    st.plotly_chart(fig)

    fig = px.bar(wells_final, x='w_id', y='Correlation', facet_row='Type', color='TOTAL', title="Correlations between well volumes and seismicity")
    st.plotly_chart(fig)

    fig=go.Figure()
    fig.add_trace(px.scatter_3d(microseismic,x='Easting [m]', y='Northing [m]', z='Depth_SS [m]', size='Moment Magnitude', size_max=10, opacity=.5).data[0])
    fig.add_trace(px.scatter_3d(wells_final, x='x', y='y', z='z', color='Correlation', size='INJECTED', hover_name='Name', size_max=50).data[0])
    fig.add_trace(px.scatter_3d(wells_final, x='x', y='y', z='z', color='Correlation', size='PRODUCED', hover_name='Name', size_max=50).data[0])
    fig.update_layout(height=600, title="Spatial distribution of seismicity and wells")
    st.plotly_chart(fig)
else:
    st.info("Use the menu on the left to load the 3 input csv files.")