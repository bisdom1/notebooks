#!/usr/bin/env python
# coding: utf-8

# # 🛢️ PGK 👶 🐍 workshop
# Introduction to python data analysis with an example analysing whether there is any correlation between seismicity and production/injection in an oil field.
# 
# To run this script, you need a Python 3.x environment with **numpy**, **pandas** and **plotly**.
# 
# ## 🛠️ Recommended set-up
# There are multiple ways to install Python on your system, but for this workshop the below steps are the easiest.
# 1. Install the Anaconda python environment from the [Anaconda website](https://www.anaconda.com/products/individual). This includes python, Jupyter notebooks, and a set of pre-installed packages for data analysis and machine learning.
# 2. The **plotly** package does not come pre-installed, but can be added by:
#     1. Starting **Anaconda Prompt** (search for anaconda prompt in your windows program folder)
#     2. A window opens showing something like `(base) C:\>`. 
#     3. Type `conda install plotly` and press enter, the **plotly** library and other dependencies will be automatically installed (if this does not work, try `pip install plotly` instead).
#     4. Close the window once done.
#     
# ## 🖥️ Running python code
# In this workshop we use jupyter notebooks to easily run code and show results. You can use any text editor to write python scripts, but the interactive environment of these notebooks is a good place to start when you're new to Python. Note that Anaconda comes with a pre-installed python code editor called **Spyder** and with **jupyter** notebooks. Both can be found under the Anaconda program folder. To run jupyter:
# 1. Look for/search for **jupyter** in your programs folder (it's installed under Anaconda).
# 2. A juypter command window will open, and shortly after a browser window will be opened that brings you to the jupyter home page.
# 3. From this page, you can start a new notebook via the **New** button (top right), or you can upload and open an existing notebook file using **Upload**.
# 4. You can also use **Upload** to upload data files that you are using in your scripts.
# 
# For more info see https://jupyter-notebook.readthedocs.io/en/stable/
# 
# ## 🥅 of this workshop
# Using spreadsheet data as a basis, we will do some basic data processing and analysis to look into a microseismic dataset and a set of wells to see if there is any pattern between production/injection and seismicity. For data analysis we make use of **pandas**, a popular library for processing structured data (i.e. spreadsheets) and for plotting we make use of **plotly**, which is optimized for plotting pandas objects.
# 
# The aim of this workshop is to demonstrate some of the data processing and visualization powers of python and to show specifically some of the advantages of python over Excel.
# ___

# ## 1. Getting started: Python module imports
# By default a python session only contains the very basic functionality. You can import the specific functionality you need by importing the relevant packages. This ensures that your python session is fit-for-purpose without using too many system resources.
# 
# In this case, we will be importing pandas for data handling and part of the plotly library for plotting. Note that we can rename the packages we import for easier use.
# 
# Once we've imported a package, we can use its functions by calling the package followed by a dot and the function. For example, to use the csv file importer in pandas, type `pd.read_csv('filename.csv')`.

# In[1]:


import numpy as np  # array operations
import pandas as pd # dataframe operations
import plotly.express as px # plotting dataframes


# ## 2. Analyzing spreadsheet data: Microseismic data
# Using pandas, spreadsheet data can be quickly imported into the python environment. Both Excel files and csv files are supported, but we will be using only csv files.
# 
# Using pandas, we import a catalogue of microseismic events (date, time, location (x,y,z coordinates and event magnitude). We store this information using the variable `microseismic`. In a jupyter notebook, you can easily print the data by simply writing the variable name. In 'real' python files, this will not work (use `print(microseismic)` instead).

# In[2]:

microseismic = pd.read_csv("microseismic.csv")

# Each event is stored in a row (12958 events in total). In this case the csv file has the column titles in the first row, and these are automatically assigned to column titles in the dataframe. You can select a column using these names, e.g. `microseismic['Moment Magnitude']` will return the column with moment magnitudes.
# 
# There is _a lot_ more that can be customized when importing csv files, including using multi-level headers, automatic formatting and data conversions, filtering invalid data etc etc. To learn more there are many useful resources online, for example https://www.datacamp.com/community/tutorials/pandas-read-csv.
# 
# There is also a column with date information. This is simply text data, but this can be used to change the table into a `timeseries` object, which gives a lot of extra flexibility to filtering and editing the data. To convert this table into a timeseries object, use `pd.to_datetime(dataframe)`

# In[3]:

microseismic.index = pd.to_datetime(microseismic['Date'])

# Still looks pretty much the same, but now we can quickly answer questions like: How many events did we have in the year 2013?

# In[4]:


microseismic['2013-01-01':'2013-12-31']


# Using the column names, we can also easily filter the data based on other properties, for example listing only events above a certain moment magnitude.

# In[5]:


microseismic[microseismic['Moment Magnitude']>3]


# ## 3. Plotting dataframes - timeseries
# 
# Python has many plotting libraries, the most oldskool one being `matplotlib`, which is a 1-1 port of the plotting functionality in Matlab. However, python has much more powerful and easier-to-use plotting libraries, and [plotly express](https://plotly.com/python/plotly-express/) in particular is extremely easy to use in combination with pandas. 
# 
# Using plotly express, we can plot the timeseries and use the available columns in the dataframe to define plot properties.

# In[6]:


# For reference, an illustration of how boring matplotlib is
import matplotlib.pyplot as plt
plt.scatter(microseismic['Easting [m]'],microseismic['Northing [m]'], label='Microseismic events')


# In[7]:


px.scatter(microseismic, x='Date', y='Moment Magnitude',title='Microseismic')


# In[8]:


# Pretty boring.. Excel can do that too. Now let's color the points by depth
px.scatter(microseismic, x='Date', y='Moment Magnitude',color='Depth_SS [m]',opacity=.5, title='Microseismic')


# Looks nice, but this does not provide much information yet beyond that there are many events. However, since this is a timeseries we can also easily resample the data to look at event frequency per month for example.

# In[9]:


px.histogram(microseismic, x='Date', title='Events/day')


# We can also make the figure a bit more interactive to easily look at specific date intervals. For this we need the 'parent' library of plotly express.

# In[10]:


import plotly.graph_objects as go
fig = px.histogram(microseismic, x='Date',title='Events/day')
fig.update_xaxes(rangeslider_visible=True)
fig.show()


# ## 4. Map view, 3-D and 4-D
# We can also inspect the spatial distribution of seismicity by plotting events in a map view, still using `px.scatter` but now with the x and y coordinates as x and y axes. In addition, we can specify point size and color as a function of microseismic attributes, e.g.:
# - marker color indicating event depth
# - marker size shows event magnitude

# In[11]:


px.scatter(microseismic, x='Easting [m]', y='Northing [m]', color='Depth_SS [m]', size='Moment Magnitude', size_max=10, opacity=.5, title='Map view seismicity')


# Lots of overlapping points.. what does this look like in 3D?
# 
# 3-D scatter plots can be made using `px.scatter_3d` instead of `px.scatter`, with the extra parameter `z='Depth_SS [m]`.

# In[12]:


px.scatter_3d(
    microseismic, 
    x='Easting [m]', 
    y='Northing [m]', 
    z='Depth_SS [m]', 
    color='Depth_SS [m]', 
    size='Moment Magnitude', 
    size_max=10, 
    opacity=.5, 
    title='3D view seismicity')


# This shows some degree of event clustering, but plotting 8 years of events in 1 map does not help in showing where the real clusters are. 
# 
# We can also show the distribution of seismicity per year or per month. This requires a new column that gives for each event the month and year in which it occurred. Since the microseismic data is a time series object, we can easily group data using `.to_period('M')`. 
# 
# For the grouping to work, the time format needs to be changed to a text label, which is done with the `.index.strftime` command.
# 
# To have a '4-D' plot, we use the same `px.scatter` function as before, but now with 3 additions:
# - `animation_frame='monthyear'` to define which column to use for grouping in time
# - `range_x` and `range_y` to fix the spatial extent of the plot

# In[13]:


microseismic['monthyear'] = microseismic.to_period('M').index.strftime("%Y-%m-%d")
px.scatter(microseismic, 
           x='Easting [m]', 
           y='Northing [m]', 
           color='Depth_SS [m]', 
           size='Moment Magnitude', 
           size_max=10, 
           opacity=.5, 
           animation_frame='monthyear',
           range_x=[min(microseismic['Easting [m]']),max(microseismic['Easting [m]'])],
           range_y=[min(microseismic['Northing [m]']),max(microseismic['Northing [m]'])],
          title='Seismicity timelapse')


# The same can be done in 3-D using again `px.scatter_3d` and adding a `z=` parameter.

# In[14]:


px.scatter_3d(microseismic, 
           x='Easting [m]', 
           y='Northing [m]', 
           z='Depth_SS [m]',
           color='Depth_SS [m]', 
           size='Moment Magnitude', 
           size_max=10, 
           opacity=.5, 
           animation_frame='monthyear',
           range_x=[min(microseismic['Easting [m]']),max(microseismic['Easting [m]'])],
           range_y=[min(microseismic['Northing [m]']),max(microseismic['Northing [m]'])],
           range_z=[min(microseismic['Depth_SS [m]']),max(microseismic['Depth_SS [m]'])],
             title='3-D seismicity timelapse')


# To keep better track of the 'center of gravity' of microseismic events, use `animation_group`, which calculates the average of each time step.

# In[15]:


px.scatter(microseismic, 
           x='Easting [m]', 
           y='Northing [m]', 
           color='Depth_SS [m]', 
           size='Moment Magnitude', 
           size_max=30, 
           opacity=.5, 
           animation_frame='monthyear',
           animation_group='monthyear',
           range_x=[min(microseismic['Easting [m]']),max(microseismic['Easting [m]'])],
           range_y=[min(microseismic['Northing [m]']),max(microseismic['Northing [m]'])],
          title='Seismicity focal point')


# Another way of looking at spatial clustering is using `px.density_contour` or `px.density_heatmap`.

# In[16]:


px.density_contour(microseismic, 
           x='Easting [m]', 
           y='Northing [m]', 
           animation_frame='monthyear',
           animation_group='monthyear',
           range_x=[min(microseismic['Easting [m]']),max(microseismic['Easting [m]'])],
           range_y=[min(microseismic['Northing [m]']),max(microseismic['Northing [m]'])],
           title='Seismicity contour map')


# ## 5. Well location data
# Now that we have a reasonable understanding of what the microseismic data looks like, we can bring in the well data, which is stored in files:
# - well_locations.csv contains the well names, types and (TD) coordinates.
# - well_rates.csv contains for each well and each time step the injection/production volumes

# In[17]:

well_locations = pd.read_csv("well_locations.csv")

# There are 3 types of wells. Using the column `Type` with the keyword `facet_col`, the locations of these 3 well types can be plotted separately.

# In[18]:

px.scatter(well_locations, x='x', y='y', color='z', hover_name='Name', facet_col='Type',title='Well locations')

# The well locations can be shown in 3-D and compared with the distribution of seismic events. 
# 
# This requires combining 2 separate dataframes into 1 figure, for which we need a Plotly Figure object. The details of the code below are outside the scope of this short session.

# In[19]:


fig=go.Figure()
fig.add_trace(px.scatter_3d(microseismic,x='Easting [m]', y='Northing [m]', z='Depth_SS [m]', color='Depth_SS [m]', size='Moment Magnitude', size_max=10).data[0])
fig.add_trace(px.scatter_3d(well_locations, x='x', y='y', z='z', color='z', hover_name='Name').data[0])
fig.show()


# ## 6. Well volumes
# Now we can see which wells are close to clusters of seismicity, but to study the relation between seismicity and production/injection, we need to know the injected/produced volumes per well. This information is stored in a separate spreadsheet, which contains monthly produced/injected volumes for oil, water and steam.
# 
# Each row lists these volumes for a given month and a given well.

# In[20]:

well_volumes = pd.read_csv("well_volumes.csv")


# To get an idea of what type of data is here, it's good practice to start with plotting the data. In Excel, this would be complicated since all data for all wells are stored in a single table. However, with pandas and plotly we can group the data per well while plotting. 
# 
# We now use `px.line` to plot rates as lines, which works similar as `px.scatter`.
# 
# As an example, we plot oil production per well. To get the plot to show each well, we use the `color` keyword. When continuous data is assigned to this keyword, data will be coloured by value but not grouped, as we could see when plotting for example seismic event depth. However, when giving categorical data to the `color` keyword, data is automatically grouped.
# 
# As we are plotting oil production, we want to plot only the producer wells, which can be done by filtering the dataframe based on oil volume injected: `well_volumes[well_volumes['OIL']>0]`

# In[21]:

well_volumes['START_DATE'] = pd.to_datetime(well_volumes['START_DATE'])
px.line(well_volumes[well_volumes['OIL']>0],x='START_DATE',y='OIL',color='HOLE_NAME',title='Oil production per well')

# ## 7. Field-wide comparison of seismicity and production/injection
# Using the well_volumes data, we can investigate whether there is a relation between seismicity and injection/production using field-wide averages.
# 
# The well volume data lists produced oil and water volumes and injected steam and water volumes. For comparing volumes to seismicity, it is helpful to also have the total injected/produced volumes. We add a few columns, which can be done in different ways:
# - simply add values of 1 column to values of another column using `+`
# - select a subset of columns and sum those using `well_volumes[['col1','col2']].sum(axis=1)` (note the double `[[` `]]`!).
# 
# We also make a column of the total, where injected volumes are negative, and produced volumes positive.

# In[22]:


well_volumes['INJECTED'] = well_volumes['STEAM_INJECTION'] + well_volumes['WATER_INJECTION']
well_volumes['PRODUCED'] = well_volumes[['OIL','WATER']].sum(axis=1)
well_volumes['TOTAL'] = -well_volumes['INJECTED'] + well_volumes['PRODUCED']

# Now we can also have a look at the field-wide injected and produced volumes as a function of time. In the table above, we have for each well for each time step the total injected. Using `groupby(by='column_name')` we can get the sum of all wells per time step.

# In[23]:


well_volumes.groupby(by='START_DATE').sum()


# Plot the totals as a function of time, where < 0 means that at that time, there was more injected than produced.

# In[24]:


fieldwide_volumes = well_volumes.groupby(by='START_DATE').sum()
fieldwide_volumes['date'] = fieldwide_volumes.index
px.line(fieldwide_volumes,x='date',y='TOTAL',title='Field-wide injection/production balance')


# We now have field-wide volumes per month and seismicity per month. To make a 1-1 comparison between these, we put them into 1 dataframe.
# 
# Since the well volumes are per month, we aggregate the seismic events per month as well by using `.resample('M')`, where `M` is for monthly resampling (`D` for per-day, `W` for per-week).

# In[25]:


microseismic['Events'] = 1 # add a field for storing event counts
ms_fieldwide = microseismic[['Events']].resample('M').count() # resample microseismic to events per month

# Now seismic data and well volumes are per month, so they can be merged together. To do so, however, we need to slightly reformat the dates, since microseismic dates are the **last days of the month** whereas well volumes are listed by the **first day** of each month.
# 
# Since both objects are timeseries, we can use `.to_period('M')` to create an index for both in the same format of Year-Month.

# In[26]:


ms_fieldwide.index = ms_fieldwide.to_period('M').index
fieldwide_volumes.index = fieldwide_volumes.to_period('M').index


# Now seismicity per month can be added to fieldwide_volumes using `pd.merge()`, which can be used to merge any 2 dataframes. We merge by index values, using the keywords `left_index` and `right_index`.

# In[27]:


merged = pd.merge(fieldwide_volumes, ms_fieldwide, left_index=True, right_index=True)


# We can also look at the injected and produced volumes of the different fluids. We already have different columns for each fluid, but to plot these different fluid volumes in 1 figure, the table needs some reshaping using `.melt()`

# In[28]:


melted = merged.melt(id_vars='date')


# In[29]:


px.line(melted,x='date',y='value',color='variable', title='Field-wide rates')


# Ok, here we reach a limit in what we can do with `plotly.express`, and we need to call in `plotly` itself to plot seismicity on a secondary y-axis to better see the relation between seismicity and injection/production volumes. 
# 
# Using plotly requires a bit more code and might take a bit more time to get used to, but it is extremely powerful and versatile. See for more details and examples the [plotly website](https://plotly.com/python/).

# In[30]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=merged['date'],y=merged['OIL'],name='Oil',yaxis='y1'))
fig.add_trace(go.Scatter(x=merged['date'],y=merged['WATER'],name='Water',yaxis='y1'))
fig.add_trace(go.Scatter(x=merged['date'],y=merged['WATER_INJECTION'],name='Water injection',yaxis='y1'))
fig.add_trace(go.Scatter(x=merged['date'],y=merged['STEAM_INJECTION'],name='Steam injection',yaxis='y1'))
fig.add_trace(go.Scatter(x=merged['date'],y=merged['INJECTED'],name='Total injection',yaxis='y1'))
fig.add_trace(go.Scatter(x=merged['date'],y=merged['PRODUCED'],name='Total production',yaxis='y1'))
fig.add_trace(go.Scatter(x=merged['date'],y=merged['Events'],name='Events',yaxis='y2',line=dict(dash='dash',color='black')))
fig.update_layout(
        yaxis1=dict(
            title="Injected/produced volumes [m3]",
        ),
        yaxis2=dict(
            title="Events",
            anchor='free',
            overlaying='y',
            side='right',
            position=1
        ),
    legend_orientation='h',
    title='Field-wide seismicity vs. injection/production'
)
fig.show()


# The above figure helps to qualitatively assess whether there is a relation between well volumes and seismicity. Calculating the correlation coefficient between these parameters provides a more quantitative measure. Below are some examples.

# In[31]:


px.scatter_matrix(merged)


# In[32]:


correlation_matrix = merged.corr()


# In[33]:


mat = correlation_matrix.values
mat[mat==1] = np.nan
mat[np.tril_indices(mat.shape[0], -1)] = np.nan
fig = go.Figure(
        data=go.Heatmap(
            z=mat, # 
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            zmin=-1,
            zmid=0,
            zmax=1,
            # hoverongaps = False,
            colorscale='RdBu',
            reversescale=True,
            colorbar=dict(
                nticks=3,
                ticktext=["negative","no corr.","positive"],
                tickmode='array',
                tickvals=[-1,0,1],
            ),
        )
    )
fig.update_layout(
    title='Correlation heatmap',
    height=600,
    width=600
)
fig.show()


# ## 8. Per-well comparison of injected/produced volumes vs. seismicity
# From the previous figure showing field-wide volumes and seismicity rates, there is no convincing relation. However, seismicity might be triggered by local injection or production - there was some clustering in the spatial distribution of seismic events - and these fieldwide aggregate values hide any local variations. 
# 
# In this part, we calculate the total injected/produced data per well through the following steps:
# 1. Define a common well identifier column for the `well_locations` dataframe and the `well_volumes` dataframe.
# 2. Use `groupby()` to group the volumes per well.
# 3. Merge the locations and grouped well volumes data.
# 
# **Step 1a: Create a well identifier and assign it as index for the well location dataframe.**

# In[34]:


well_locations['w_id'] = well_locations['Name'].str.replace('PGKYP','')
well_locations.index = well_locations['w_id']


# **Step 1b: Do the same for the well_volumes dataframe:**

# In[35]:


well_volumes[['prefix','w_id']] = well_volumes['HOLE_NAME'].str.split('-',expand=True)


# **Step 2: Group the data to get cumulative volumes per well**

# In[36]:


summed_volumes = well_volumes.groupby(by='w_id').sum()


# **Step 3: Merge well volumes with well locations**

# In[37]:


wells = pd.merge(well_locations, summed_volumes, left_index=True, right_index=True)


# In[38]:


fig=go.Figure()
fig.add_trace(px.scatter_3d(microseismic,x='Easting [m]', y='Northing [m]', z='Depth_SS [m]', size='Moment Magnitude', size_max=10).data[0])
fig.add_trace(px.scatter_3d(wells, x='x', y='y', z='z', color='INJECTED', size='INJECTED', hover_name='Name').data[0])
fig.add_trace(px.scatter_3d(wells, x='x', y='y', z='z', color='PRODUCED', size='PRODUCED', hover_name='Name').data[0])
fig.show()


# ## 9. Correlation between well volumes and seismicity
# The final step is to further quantify the observations from the 3-D plot above by calculating the correlation coefficient between the volume injected/produced in each well and the number of seismic events.
# 
# For this we go back to well_volumes and we use `pivot_table()` to get a table with a row for each time step and a column for each well.

# In[39]:


# In[40]:


volume_per_well = well_volumes.pivot_table(index='START_DATE',columns='w_id',values='TOTAL')
volume_per_well.index = volume_per_well.index.to_period('M') 
volume_per_well.fillna(0,inplace=True)


# This table can be readily merged with the table of microseismic event counts per month that we created earlier (`ms_fieldwide`)

# In[41]:


merged_final = pd.merge(ms_fieldwide, volume_per_well, left_index=True, right_index=True)


# Similar to before, we can use `corr()` to calculate the correlation coefficients between the volumes injected/produced by each well and the seismicity.

# In[42]:


corr_per_well = merged_final.corr()
corr_per_well['labels'] = corr_per_well.columns # some cleaning up/formatting for plotting 
corr_per_well[corr_per_well == 1] = np.nan

# In[43]:


px.bar(corr_per_well, x='labels', y='Events', labels={'Events': 'Correlation','labels': 'Well'}, title='Seismicity vs well volume').update_xaxes(categoryorder='total descending')


# We can see that wells 33 and 24 have a relatively strong correlation between well rate and seismicity. To better understand what type of wells these are and where they are, we add the correlations to the wells spreadsheet.

# In[44]:


wells_final = pd.merge(wells, corr_per_well[['Events']], left_index=True, right_index=True)
wells_final = wells_final.rename(columns = {'Events':'Correlation'}) # rename a column name


# We can again make the bar plot, and now color the bars by well type

# In[45]:


px.bar(wells_final, x='w_id', y='Correlation', color='Type')


# Or use `facet_row` to make subplots based on well type, and now color the bars based on total volume injected/produced.

# In[46]:


px.bar(wells_final, x='w_id', y='Correlation', facet_row='Type', color='TOTAL')


# Finally, we can plot again seismicity in 3-D and add the well locations, with:
# - symbol size scaled by the total volume injected/produced
# - symbol color indicating the correlation between injected/produced volume and seismicity.

# In[47]:


fig=go.Figure()
fig.add_trace(px.scatter_3d(microseismic,x='Easting [m]', y='Northing [m]', z='Depth_SS [m]', size='Moment Magnitude', size_max=5, opacity=.5).data[0])
fig.add_trace(px.scatter_3d(wells_final, x='x', y='y', z='z', color='Correlation', size='INJECTED', hover_name='Name', size_max=50).data[0])
fig.add_trace(px.scatter_3d(wells_final, x='x', y='y', z='z', color='Correlation', size='PRODUCED', hover_name='Name', size_max=50).data[0])
fig.show()


# All of the tables that we generated can be exported to Excel files using `object_name.to_csv("filename.csv")`

# In[48]:


wells_final.to_csv("wells_final.csv")


# # 🏁 Conclusions
# Based on the available data, there is no clear relation between seismicity and injection/production. As per usual, we need more data.

# In[ ]:




