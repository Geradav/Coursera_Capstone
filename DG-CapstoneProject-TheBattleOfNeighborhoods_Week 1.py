#%% [markdown]
#
# I propose to work with the data of the city of Kampala, Uganda.
#
# First we are going to review some available data about Uganda.

#%%
# Importing all required libraries
import numpy as np
import pandas as pd
import folium

print('Done importing the required modules!')

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
#
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
print(df_PopInternet.head(), '\n')

# Let's rename the 'Central' column in 'District'
df_PopInternet.rename(columns={'Central':'District'}, inplace=True)
# Let's keep Uganda country data separately from the district data
Uganda_Internet = df_PopInternet[df_PopInternet['District'] == 'Uganda'].drop(columns=['Region'])
df_PopInternet.dropna(subset=['Total'], inplace=True)
df_PopInternet.drop(index=df_PopInternet[df_PopInternet['District'] == 'Uganda'].index, inplace=True)
print(Uganda_Internet, '\n\n', df_PopInternet.head(5), '\n\n', df_PopInternet.tail())

#%%

df_PopComputer.rename(columns={'Unnamed: 0': 'District', 'Male':'Male Headed Households', 'Female': 'Female Headed Households'}, inplace=True)
df_PopComputer.drop(index=[0,1], inplace=True)
df_PopComputer.head()

#%%
df_PopComputer.reset_index(drop=True, inplace=True)

RegionCol2 = []
for I, district, total in zip(df_PopComputer.index, df_PopComputer['District'], df_PopComputer['Total']):
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
df_PopComputer.dropna(subset=['Total'], inplace=True)
df_PopComputer.drop(index=df_PopComputer[df_PopComputer['District'] == 'Uganda'].index, inplace=True)

print('Head view of the data (Computer):\n\n', df_PopComputer.head(), '\n\n\nTail view of hte data (computer):\n\n', df_PopComputer.tail(), '\n')

#%%
# Let's first rename the 'Region' column in 'District'
df_PopMobilePhone.rename(columns={'Region': 'District'}, inplace=True)
df_PopMobilePhone.reset_index(drop=True, inplace=True)

RegionCol3 = []
for I, district, total in zip(df_PopMobilePhone.index, df_PopMobilePhone['District'], df_PopMobilePhone['Total']):
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
df_PopMobilePhone.dropna(subset=['Total'], inplace=True)
df_PopMobilePhone.drop(index=df_PopMobilePhone[df_PopMobilePhone['District'] == 'Uganda'].index, inplace=True)

print('Head view of the data (MobilePhone):\n\n', df_PopMobilePhone.head(), '\n\n\nTail view of the data (MobilePhone):\n\n', df_PopMobilePhone.tail(), '\n')

#%%
print('Computer dataframe shape:\n\n', df_PopComputer.shape, '\n\n\nInternet dataframe shape:\n\n', df_PopInternet.shape, '\n\n\nMobile phone dataframe shape:\n\n', df_PopMobilePhone.shape)

#%%
# Let's continue with the population dataset
#
df_PopSize.rename(columns={'Region': 'District', 'Unnamed: 1': 'Households', 'Household': 'Household population', 'Average':'Average household size', 'Female': 'Female Headed', 'Child': 'Child headed', 'Non Household': 'Non household population'}, inplace=True)

# Drop the first two rows
df_PopSize.drop([0,1], inplace=True)
df_PopSize.head()

#%%
df_PopSize.reset_index(drop=True, inplace=True)

df_PopSize['Households'] = pd.to_numeric(df_PopSize['Households'].str.replace(',', ''), errors='coerce')
df_PopSize['Household population'] = pd.to_numeric(df_PopSize['Household population'].str.replace(',', ''), errors='coerce')

RegionCol4 = []
for I, district, household in zip(df_PopSize.index, df_PopSize['District'], df_PopSize['Households']):
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
df_PopSize.drop(index=df_PopSize[df_PopSize['District'] == 'UGANDA'].index, inplace=True)
df_PopSize.drop(index=df_PopSize[df_PopSize['District'] == 'Region'].index, inplace=True )

print('Head view of the data (Population size):\n\n', df_PopSize.head(), '\n\n\nTail view of the data (Population size):\n\n', df_PopSize.tail(), '\n')


#%%
from geopy.geocoders import Nominatim
UgApp = Nominatim(user_agent='UgApp')
UgLoc = UgApp.geocode('Uganda',)
UgLat = UgLoc.latitude
UgLong = UgLoc.longitude

print('Coordinates: ', UgLoc, '\n\nLatitude: ', UgLat, '\n\nLongituted: ', UgLong)


#%%
# import GeoJson
UgMap = folium.Map(location=[UgLat, UgLong], zoom_start=7)
GeoJSON_Abim = 'Abim.geojson'

# folium.GeoJson(GeoJSON_UG).add_to(UgMap)
Acholi = folium.FeatureGroup(name='Acholi')
folium.Choropleth(
    geo_data=GeoJSON_Abim
).add_to(Acholi)
Acholi.add_to(UgMap)
folium.LayerControl().add_to(UgMap, name='Ug layer')

UgMap

#%%
