#%% [markdown]
# # Capston Week 1
#  ***David Gerard***  
#   
#   
# In Uganda, an organization is trying to develop modern solutions using the Internet and connected devices. 
# There is a lot to do and for a start, we would like to know a bit better the proportion of the population 
# that has a mobile phone, has a computer, and access to the Internet. We also want to learn about their 
# online activities and habits so that we can refine our understanding of the market and better concentrate 
# our efforts around our offers, and our marketing strategy.
# First, we will download and process some data available online about ownership of the computer, mobile 
# phones, and access to the Internet. Then, we will try and plot those data on a map to better visualize where 
# those users are concentrated. We will concentrate around the central region as we want to be close to our 
# operation HQ and minimize costs.
#
# First we are going to review some available data about Uganda.  
# 
# Then we will concentrate on the Central region
#
# _____
# _____
#%%
# Importing all required libraries
import numpy as np
import pandas as pd
import folium

print('Done importing the required modules!')

#%% [markdown]
# 
# After importing all necessary libraries, we access the files online and pass them to a Pandas DataFrame.
# 
# _____

#%%
# Accessing the data files
df_PopInternet = pd.read_csv('https://www.ubos.org/wp-content/uploads/statistics/Population_aged_10_years_+_using_Internet_by_Region_and_District_NPHC_2014.csv')
df_PopComputer = pd.read_csv('https://www.ubos.org/wp-content/uploads/statistics/Percent_of_Population_aged_10_years_+_with_a_computer_by_Region_and_District_NPHC_2014.csv')
df_PopMobilePhone = pd.read_csv('https://www.ubos.org/wp-content/uploads/statistics/Percent_of_Population_aged_10_years_+_owning_a_mobile_phone.csv')
df_PopSize = pd.read_csv('https://www.ubos.org/wp-content/uploads/statistics/Selected_Indicators_(Household_Population,_Hhds,_Avg_HHd_Size,_)_by_District___2002_Census.csv')

print('All dataframes are now accessible')
# Let's have a quick look at each dataframe
print('\n')
print('Population with access to Internet.\n', df_PopInternet.head(), '\n')
print('Population with access to a computer.\n', df_PopComputer.head(), '\n')
print('Population with access to a mobile phone.\n', df_PopMobilePhone.head(), '\n')
print('Population size.\n', df_PopSize.head())

#%% [markdown]
#
# We can see that the data needs some manipulation, some cleansing.  
# The Region is in the same column as the district.  
# We are going to extract it and create a column Region for each record.  
# We are going to rename the headers.  
# And then we will delete rows for which the Total is NaN
# _____
#

#%% [markdown]
# 
# ## Internet dataset preparation
# _____

#%%
df_PopInternet.reset_index(drop=True, inplace=True)

RegionCol = []
for I, central, total in zip(df_PopInternet.index, df_PopInternet['Central'], df_PopInternet['Total']):
    if I == 0:
        varRegion = 'Central'
        RegionCol.append(varRegion)
    else:
        if np.isnan(total):
            varRegion = central
            RegionCol.append(varRegion)
        else:
            RegionCol.append(varRegion)
df_PopInternet['Region'] = RegionCol

# Let's rename the 'Central' column in 'District'
df_PopInternet.rename(
    columns={'Central':'District'},
    inplace=True
)

# Let's keep Uganda country data separately from the district data
Uganda_Internet = df_PopInternet[df_PopInternet['District'] == 'Uganda'].drop(columns=['Region'])
df_PopInternet.dropna(
    subset=['Total'],
    inplace=True
)
df_PopInternet.drop(
    index=df_PopInternet[df_PopInternet['District'] == 'Uganda'].index,
    inplace=True
)

print(
    Uganda_Internet,
     '\n\n',
      df_PopInternet.head(5),
       '\n\n',
        df_PopInternet.tail()
)

#%% [markdown]
# 
# ## Computer dataset preparation  
# 
# _____
# 
#%%

df_PopComputer.rename(
    columns={
        'Unnamed: 0': 'District',
         'Male':'Male Headed Households',
          'Female': 'Female Headed Households'
    },
     inplace=True
)
df_PopComputer.drop(index=[0,1], inplace=True)
df_PopComputer.head()

df_PopComputer.reset_index(drop=True, inplace=True)

RegionCol2 = []
for I, district, total in zip(
    df_PopComputer.index,
     df_PopComputer['District'],
      df_PopComputer['Total']
    ):
    if I == 0:
        varRegion2 = 'Central'
        RegionCol2.append(varRegion2)
    else:
        if np.isnan(total):
            varRegion2 = district
            RegionCol2.append(varRegion2)
        else:
            RegionCol2.append(varRegion2)
df_PopComputer['Region'] = RegionCol2


# Let's keep Uganda country data separately from the district data
Uganda_Computer = df_PopComputer[df_PopComputer['District'] == 'Uganda'].drop(columns=['Region'])
df_PopComputer.dropna(
    subset=['Total'],
     inplace=True
)
df_PopComputer.drop(
    index=df_PopComputer[df_PopComputer['District'] == 'Uganda'].index,
     inplace=True
)

print(
    'Head view of the data (Computer):\n\n',
     df_PopComputer.head(),
      '\n\n\nTail view of the data (computer):\n\n',
       df_PopComputer.tail(),
        '\n'
)

#%% [markdown]
# 
# ## MobilePhone dataset preparation  
# 
# _____
#%%
# Let's first rename the 'Region' column in 'District'
df_PopMobilePhone.rename(
    columns={'Region': 'District'},
    inplace=True
)
df_PopMobilePhone.reset_index(
    drop=True,
     inplace=True
)

RegionCol3 = []
for I, district, total in zip(
    df_PopMobilePhone.index,
     df_PopMobilePhone['District'],
      df_PopMobilePhone['Total']
    ):
    if I == 0:
        varRegion3 = 'Central'
        RegionCol3.append(varRegion3)
    else:
        if np.isnan(total):
            varRegion3 = district
            RegionCol3.append(varRegion3)
        else:
            RegionCol3.append(varRegion3)
df_PopMobilePhone['Region'] = RegionCol3

# Let's keep Uganda country data separately from the district data
Uganda_MobilePhone = df_PopMobilePhone[df_PopMobilePhone['District'] == 'Uganda'].drop(columns=['Region'])
df_PopMobilePhone.dropna(
    subset=['Total'],
     inplace=True
)
df_PopMobilePhone.drop(
    index=df_PopMobilePhone[df_PopMobilePhone['District'] == 'Uganda'].index,
    inplace=True
)

print(
    'Head view of the data (MobilePhone):\n\n',
     df_PopMobilePhone.head(),
      '\n\n\nTail view of the data (MobilePhone):\n\n',
       df_PopMobilePhone.tail(),
        '\n'
)

#%% [markdown]
#  
# Let's review the shape of each dataframe for the three datasets we have processed so far

#%%

print(
    'Computer dataframe shape:\n\n',
    df_PopComputer.shape,
    '\n\n\nInternet dataframe shape:\n\n',
    df_PopInternet.shape,
    '\n\n\nMobile phone dataframe shape:\n\n',
    df_PopMobilePhone.shape
)
#%% [markdown]
# 
# ## Population dataset preparation  
# 
# _____
# 

#%%
# Let's continue with the population dataset
#
df_PopSize.rename(
    columns={
        'Region': 'District',
        'Unnamed: 1': 'Households',
        'Household': 'Household population',
        'Average':'Average household size',
        'Female': 'Female Headed',
        'Child': 'Child headed',
        'Non Household': 'Non household population'
    },
     inplace=True
)

# Drop the first two rows
df_PopSize.drop([0,1], inplace=True)
df_PopSize.head()

df_PopSize.reset_index(
    drop=True,
    inplace=True
)

df_PopSize['Households'] = pd.to_numeric(df_PopSize['Households'].str.replace(',', ''), errors='coerce')
df_PopSize['Household population'] = pd.to_numeric(df_PopSize['Household population'].str.replace(',', ''), errors='coerce')

RegionCol4 = []
for I, district, household in zip(
    df_PopSize.index,
    df_PopSize['District'],
    df_PopSize['Households']
):
    if I == 0:
        varRegion4 = 'Central'
        RegionCol4.append(varRegion4)
    else:
        if np.isnan(household):
            varRegion4 = district
            RegionCol4.append(varRegion4)
        else:
            RegionCol4.append(varRegion4)
df_PopSize['Region'] = RegionCol4

# Let's keep Uganda country data separately from the district data
Uganda_PopSize = df_PopSize[df_PopSize['District'] == 'UGANDA'].drop(columns=['Region'])
Region_PopSize = df_PopSize[df_PopSize['District'] == 'Region']
df_PopSize.dropna(subset=['Households'], inplace=True)
df_PopSize.drop(
    index=df_PopSize[df_PopSize['District'] == 'UGANDA'].index,
    inplace=True
)
df_PopSize.drop(
    index=df_PopSize[df_PopSize['District'] == 'Region'].index,
    inplace=True
)

print('Head view of the data (Population size):\n\n', df_PopSize.head(), '\n\n\nTail view of the data (Population size):\n\n', df_PopSize.tail(), '\n')

#%% [markdown]
# 
# Now that we have the data ready we can work on the map
# 

#%% [markdown]
# 
# ## Map preparation  
# 
# _____

#%%
from geopy.geocoders import Nominatim
UgApp = Nominatim(user_agent='UgApp')
UgLoc = UgApp.geocode('Uganda',)
UgLat = UgLoc.latitude
UgLong = UgLoc.longitude

print('Coordinates of Uganda: ', UgLoc, '\n\nLatitude: ', UgLat, '\n\nLongituted: ', UgLong)

#%% [markdown]
# 
# Let's see Uganda on a map
#%%

UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)
UgMap

#%% [markdown]
# 
# Now we are going to use a GeoJSON file to plot the districts on the map using Choropleth from Folium.
# We are going to parse it to access its properties and mainly the subregion
# 
#%%
GeoJSON_Ug = 'ugandadistricts.geojson'
UgDict = open(GeoJSON_Ug).read()

import json
Ug_Gjson_Data = json.loads(open(GeoJSON_Ug).read())

#%% [markdown]
# 
# Now we can display our districts on a map with a choropleth layer
#  and visualize the different datasets we have prepared.
# We will concentrate on the subregions Central 1 and Central 2
#
#%% [markdown]
# 
# ## Population dataset - Map visualisation  
# 
# _____
# _____
#%% [markdown]
# 
# ### Central 1
# _____

#%%

UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    fg_acholi = folium.FeatureGroup(
            name='Acholi', show= False
        ) if not fg_acholi == True else None
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 1':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopSize,
    columns=['District', 'Households'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# ### Central 2 
# _____
#%%
UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 2':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopSize,
    columns=['District', 'Households'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# ## Computer dataset
# 
# _____
# _____

#%% [markdown]
# 
# ### Central 1
# _____

#%%
UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 1':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopComputer,
    columns=['District', 'Total'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# ### Central 2
# _____
# 
#%%
UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 2':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopComputer,
    columns=['District', 'Total'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%%[markdown]
# 
# ## Internet dataset
# 
# _____
# _____

#%% [markdown]
# 
# ### Central 1
# _____
# 
#%%

UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 1':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopInternet,
    columns=['District', 'Total'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# ### Central 2
# _____

#%%
UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 2':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopInternet,
    columns=['District', 'Total'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# ## MobilePhone dataset
# 
# _____
# _____

#%% [markdown]
# 
# ### Central 1
# _____


#%%

UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 1':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopMobilePhone,
    columns=['District', 'Total'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# ### Central 2
# _____

#%%
UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)

jsonString = '{\"type\": \"FeatureCollection\",\"features\": []}'
fg_acholi = None
geojsonFile = json.loads(jsonString)
for i in range(len(Ug_Gjson_Data['features'])):
    if Ug_Gjson_Data['features'][i]['properties']['Subregion'] == 'CENTRAL 2':
        geojsonFile['features'].append(Ug_Gjson_Data['features'][i])
    else:
        pass

geoFile = json.dumps(geojsonFile)
folium.Choropleth(
    geo_data=geoFile,
    data=df_PopMobilePhone,
    columns=['District', 'Total'],
    key_on='feature.properties.District',
    fill_color='YlGn',
    popup='cool',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of households per district'
).add_to(UgMap)

UgMap

#%% [markdown]
# 
# We can see from the different maps that the Central 1 subregion and more in particular Kampala (the capital) 
# is where the population has a higher ownership of computer and mobilephones, and higher access to Internet.
# In dark grey or black are the district for which there was no data  
# 


#%%
