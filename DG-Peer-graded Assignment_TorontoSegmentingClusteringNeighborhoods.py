#%% [markdown]
# # **Peer-graded Assignment: Segmenting and Clustering Neighborhoods in Toronto**
# <br/><br/>
# *Author-Student: David Gerard*
# _____
# _____


#%% [markdown]
# We first import the libraries we need
# _____

#%%

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#%% [markdown]

#
# We can obtain the source file using the 'get' command from the requests library. 
# I first create a variable containing the link to the webpage. 
# Then I create another variable to contain the response of the 'get' command. 
# I pass the text only of the webpage into the 'WebText' variable 
# and finally I use 'BeautifulSoup()' to parse the HTML text and pass it to 'htmlContent'
# _____

#%%
WebLink = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
WebPage = requests.get(WebLink)
WebText = WebPage.text
htmlContent = BeautifulSoup(WebText)

#%% [markdown]
#
# From the 'htmlContent' we extract the table containing the data we want 
# and we pass it to the variable dataTable.
# <br/>
# We identify the table we want using the 'class' attribute 'wikitable sortable'
# _____

#%%
dataTable = htmlContent.find('table', attrs={"class":"wikitable sortable"})


#%% [markdown]

# Now that we have easy access to our web table we can iterate through each row 
# identified by the HTML tags 'tr' and extract the text from each cell.
# _____

#%%
# We can first create an array of all rows identified by the HTML tag 'tr'
tableRows = dataTable.find_all('tr')

# Now that we have an array of all rows, we can access the first element 
# and extract the headers (corresponding to the first row in the table)
# The first row is being accessed by its index (0)

TableHeaders = [] # array variable for headers initiated
for eachElement in tableRows[0].find_all('th'):
    TableHeaders.append(eachElement.text.replace('\n', '').strip())

theTable = [] # array variable for table initiated
for eachRow in tableRows:
    TableRow = {} # dictionnary variable initiated
    for eachCell, eachHeader in zip(eachRow.find_all('td'), TableHeaders): # header as key and cell data as value
        TableRow[eachHeader] = eachCell.text.replace('\n', '').strip() # remove line breaks and clean the string
    theTable.append(TableRow)

print(theTable[:5]) # print the first 5 elements of the dictionnary

#%% [markdown]

# Let's now pass the dictionnary 'theTable' into a pandas dataframe
# _____
#%%
import pandas as pd
df = pd.DataFrame(theTable)
df.head()

#%% [markdown]
# We can clean our dataframe
# <br/><br/>
# Let's apply the following:
#  - delete empty row (drop na)
#  - remove rows with 'Not assigned' value as Borough
#  - replace 'Not assigned' value in Neighbourood column with value from Borough column
#  - group by columns Postcode and Borough, and join values from Neighbouhood
# <br/><br/>
# Then we can finish by applying the .shape method to print the number of rows and columns in the dataframe

#%%
df.dropna(axis=0,inplace=True)
df = df[df.Borough !='Not assigned']
df['Neighbourhood'] = np.where(df['Neighbourhood'] == 'Not assigned', df['Borough'], df['Neighbourhood'])
dfResult = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(', '.join).reset_index()
print(dfResult.head(n=10))
print(dfResult.shape)
#%% [markdown]
#
# Now we are going to retrieve the coordinates of the different neighbouroods. 
# For that, we will use the CSV file, as importing the geocoder library failed

#%%

fileName = 'Geospatial_coordinates.csv'
coordinatesFile = pd.read_csv(fileName)
coordinatesFile.head()

#%% [markdown]
# Let's rename the column 'Postal Code' of the imported file into 'Postcode' to match to other dataframe
# We then merge both datasets together and we can do some analysis of our data.
#
#%%
coordinatesFile.rename(columns={'Postal Code':'Postcode'}, inplace=True)
dfWithCoordinates = dfResult.merge(coordinatesFile, on='Postcode')
print('First five rows in the dataset')
print(dfWithCoordinates.head())
print('')
print('Last 5 rows in the dataset')
print(dfWithCoordinates.tail())
print('')
print('The dataset for Toronto contains {} borough and {} neighborough.'.format(len(set(dfWithCoordinates['Borough'])), dfWithCoordinates.shape[0]))

#%%
BoroughAnalysis = pd.DataFrame(data=dfWithCoordinates[['Borough', 'Neighbourhood']].groupby('Borough').count()).reset_index().rename(columns={'Borough': 'Name of borough', 'Neighbourhood': 'Number of neighbourhood'})
NeighbourhoodAnalysis = dfWithCoordinates[['Borough', 'Neighbourhood']]
NeighbourhoodAnalysis['Number of neighbourhood sharing the same postal code'] = NeighbourhoodAnalysis['Neighbourhood'].str.count(', ') + 1

minBorough = BoroughAnalysis[BoroughAnalysis['Number of neighbourhood'] == BoroughAnalysis['Number of neighbourhood'].min()]
maxBorough = BoroughAnalysis[BoroughAnalysis['Number of neighbourhood'] == BoroughAnalysis['Number of neighbourhood'].max()]
moreThanOneNeighPerPC = NeighbourhoodAnalysis[NeighbourhoodAnalysis['Number of neighbourhood sharing the same postal code'] > 1]
print('The dataset contains {} borough with only {} postal code.'.format(minBorough.shape[0], minBorough['Number of neighbourhood'].min()))
print('')
print(minBorough)
print('')
print('And the dataset contains {} borough with {} postal codes.'.format(maxBorough.shape[0], maxBorough['Number of neighbourhood'].max()))
print('')
print(maxBorough)
print('')
print('Also, {} postal codes are shared by several neighbourhoods, with up to {} neighbourhoods for 1 postal code.'.format(moreThanOneNeighPerPC.shape[0], moreThanOneNeighPerPC['Number of neighbourhood sharing the same postal code'].max()))
#%%

#%% [markdown]

# Now we can plot our data on a map. 
# For that we will import the folium library. 
# We will retrive the coordinates of the city of Toronto 
# and we will display the map.

#%%
from geopy.geocoders import Nominatim
import folium
vToronto = Nominatim(user_agent="TorontoGeoLoc")
TorontoLoc = vToronto.geocode("Toronto, Canada")
TorontoCoordinates = [TorontoLoc.latitude, TorontoLoc.longitude]
TorontoMap = folium.Map(location= TorontoCoordinates, zoom_start=10)
TorontoMap

#%% [markdown]
# 
# Let's first plot all points on the map

#%%
TorontoMap = folium.Map(location= TorontoCoordinates, zoom_start=10)


for T_lat, T_lng, T_borough, T_neighbourhood in zip(dfWithCoordinates['Latitude'], dfWithCoordinates['Longitude'], dfWithCoordinates['Borough'], dfWithCoordinates['Neighbourhood']):
    label = '{}, {}'.format(T_neighbourhood, '(' + T_borough + ')')
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [T_lat, T_lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.7,
        parse_html=False).add_to(TorontoMap)

TorontoMap

#%% [markdown]
#
# Let's now give a different color to each borough
#

#%%
import randomcolor as randcol

# Retrieve unique values in the Borough field
BoroughUL = set(dfWithCoordinates['Borough'])

# Reset the map
TorontoMap = folium.Map(location= TorontoCoordinates, zoom_start=10)

# Loop through each unique borough, attribute a random color 
# and create a feature group for each borough and add them to a layer
for eachBorough1 in sorted(BoroughUL):
    labelColor1 = randcol.RandomColor().generate()[0]
    Borough_N = dfWithCoordinates[dfWithCoordinates['Borough'] == eachBorough1]
    newFeatGrp = folium.FeatureGroup(name= eachBorough1)
    for T_lat, T_lng, T_borough, T_neighbourhood in zip(Borough_N['Latitude'], Borough_N['Longitude'], Borough_N['Borough'], Borough_N['Neighbourhood']):
        label = '{}, {}'.format(T_neighbourhood, '(' + T_borough + ')')
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [T_lat, T_lng],
            radius=5,
            popup=label,
            color=labelColor1,
            fill=True,
            fill_color=labelColor1,
            fill_opacity=0.7,
            parse_html=False).add_to(newFeatGrp)
        newFeatGrp.add_to(TorontoMap)

folium.LayerControl().add_to(TorontoMap)
TorontoMap

