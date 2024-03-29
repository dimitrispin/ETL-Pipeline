
# Import the necessary modules

import requests
from sqlalchemy import create_engine
import numpy as np 
import pandas as pd 


#Extract the data from the API and convert the data to a json file

def extract():
    url = "http://universities.hipolabs.com/search?country=United+States"
    data = requests.get(url).json()
    return data
#See the data into json format
data=extract()

#Load the data into pandas dataframe, make every necessary filtering we see fit

def transform(data):
    df = pd.DataFrame(data)
    print(f"Total Number of universities from API: {len(data)}")

  #We have the domains and the web pages in a list-like format, and we change that into a comma separated format
    df['domains'] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(str, l)) for l in df['web_pages']]
  # We have to reset the index if we use the print method and not just type the df in jup. notebook
    df = df.reset_index(drop=True)
# Remove columns with more than 50% NaN values
    missing_columns = df.loc[:, df.isna().mean() >= 0.5].columns
    df= df.drop(missing_columns, axis=1)
    df.rename(columns= {'alpha_two_code' : 'acronym'})
    return df

df = transform(data)
df

# We load the data into a sqllite database or any database that we might have
def load(df):
    disk_engine = create_engine('sqlite:///my_lite_store.db')
# We basically convert the dataframe into a table called unis
    df.to_sql('unis', disk_engine, if_exists='replace')
load(df)
