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
htmlContent = BeautifulSoup(WebText, 'lxml')

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
dfResult = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(','.join).reset_index()
print(dfResult.head(n=10))
print(dfResult.shape)
#%%
