"""
This module is used to fetch the listings from Makaan.com using the scraper and to store the data
in a local MongoDB Server.
Makaan.com URLS for Different Regions of Delhi
Active as of 7.6.20
'https://www.makaan.com/delhi/delhi-east-flats-for-rent-10019?page=1'
'https://www.makaan.com/delhi/rohini-flats-for-rent-11606?page=1'
'https://www.makaan.com/delhi/delhi-south-flats-for-rent-10022?page=1'
'https://www.makaan.com/delhi/west-delhi-flats-for-rent-10176?page=1'
'https://www.makaan.com/delhi/north-delhi-flats-for-rent-10177?page=1'
'https://www.makaan.com/delhi/dwarka-flats-for-rent-10212?page=1'
https://www.makaan.com/delhi/delhi-central-flats-for-rent-10018?page=1
The following listings have very little data or many outliers (Ignore).
https://www.makaan.com/delhi/other-flats-for-rent-10571?page=1
https://www.makaan.com/delhi/south-west-delhi-flats-for-rent-11473?page=1
https://www.makaan.com/delhi/delhi-north-flats-for-rent-10558?page=1
https://www.makaan.com/delhi/north-west-delhi-flats-for-rent-11475?page=1
https://www.makaan.com/delhi/delhi-west-flats-for-rent-10559?page=1
"""

from Scraper.Makaan_scraper import listings_to_df
from pymongo import MongoClient
import pandas as pd

# Create the pymongo MongoDB driver client and pass the IP and port.

client = MongoClient('mongodb://127.0.0.1:27017/')

# Create a new Database or Load one

data = client['Makaan_rental_listings']

# Create a Table or Collection

rent_prices = data.rent_prices

listings = listings_to_df('https://www.makaan.com/delhi/delhi-west-flats-for-rent-10559?page=1', num_pages=200)
data_dict = listings.to_dict(orient='records')

rent_prices.insert_many(data_dict)

# Transferring Data from mongoDB collection to PD DF is straight-forward, just return all records using collection and
# the cursor that is returned needs to converted to a list.
# problems when nested JSON objects, then have to use json normalise.

dataframe = pd.DataFrame(list(rent_prices.find({})))
dataframe.drop(['_id'], axis = 1, inplace=True)
dataframe.set_index(['id'], inplace=True)
dataframe.to_csv("Data/June_8_data.csv")