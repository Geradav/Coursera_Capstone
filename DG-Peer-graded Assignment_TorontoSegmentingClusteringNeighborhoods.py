#%%
from bs4 import BeautifulSoup
import requests
WebDataSource = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M").text

type(WebDataSource)


#%%
wds = BeautifulSoup(WebDataSource, 'lxml')

#%%
print(wds.prettify())

#%%
TableContent = wds.find('table', attrs={"class":"wikitable sortable"})
TableContent_Data = TableContent.tbody.find_all("tr")


#%%
TableHeader = []
for th in TableContent_Data[0].find_all("th"):
    TableHeader.append(th.text.replace('\n', '').strip())

print(TableHeader)


#%%
TableData = {}
T_Headers = []
for th in TableContent_Data[0].find_all('th'):
    T_Headers.append(th.text.replace('\n', '').strip())
T_Data = []
for tr in TableContent_Data:
    Table_Row = {}
    for td, th in zip(tr.find_all('td'), T_Headers):
        Table_Row[th] = td.text.replace('\n', '').strip()
    T_Data.append(Table_Row)

print(T_Data)

#%%
import pandas as pd
dataFrame = pd.DataFrame(T_Data)
dataFrame.head()

#%%
