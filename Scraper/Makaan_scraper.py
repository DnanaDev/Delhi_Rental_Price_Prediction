"""
Makaan.com - Has props for rent in different parts of Delhi,
This script contains functions that take in the first page of a query result and scrapes
the following data fields from the JSON file embedded in the listings:
'id' - listing ID make sure no duplicates.
'size' - sq feet
'propertyType'
"bedrooms"
'latitude'
'longitude'
'localityName'
'suburbName'
'cityName'
'price'
'companyName'

Function to return the scraped data in the form of a Pandas Dataframe.

Other:
Sample Config JSON in Listing:
{"selector":"listing_10051927","sellerType":"AGENT",
 "companyType":"AGENT","companyId":2068867,"companyUserId":17937939,
 "backgroundColor":"#dde2ed","textColor":"#fff","nameText":"S",
 "companyName":"Smart Homes","companyRating":4.3,
 "verificationDate":1588444200000,"serverTime":1591379468463,
 "listingUrl":"https://www.makaan.com/delhi/builder-project-in-sainik-farms-10051927/2bhk-3t-1500-sqft-independenthouse-for-rent",
 "imageUrl":"https://static.makaan.com/17/0/572/31067456.jpeg?width=460&amp;height=260"
 ,"id":10051927,"propertyId":10581254,"projectId":1187264,"projectName":"Project",
 "projectStatus":"Ready to move","mainImageId":"","imageCount":0,"latitude":28.50962448,"longitude":77.19683838
 ,"localityName":"Sainik Farms","suburbName":"Delhi South","cityName":"Delhi"
 ,"localityUrl":"https://www.makaan.com/delhi/sainik-farms-real-estate-53815"
 ,"rank":7,"price":35000,"unitTypeId":19,"propertyType":"Independent House","bedrooms":2
 ,"isPlot":false,"isApartment":false,"localityId":53815,"suburbId":10022,"cityId":6
 ,"listingScore":4.18182,"listingCategory":"Rental","isCommercial":""
 ,"size":"1,500 sq ft","isRk":false,"isPentHouse":false,"isStudio":false,"defaultImageId":""
 ,"sellerCallRatingCount":0,"sellerCompanyFeedbackCount":0,"isAccountLocked":false
 ,"isPaidSeller":false,"sellerTransactionStatus":{"isExpertDealMaker":false
                                                  ,"isDealMaker":false,"typeLabel":""}
 ,"isOriginalSearchResult":true,"isMakaanSelectSeller":false,"mainImageWidth":584,"mainImageHeight":330
 ,"leadType":"paid","reraInfo":"N/A","isMPMatchTagListing":"false","listingDomain":"housing"}
"""

import json
import pandas as pd
from bs4 import BeautifulSoup
import requests


def fetch_listings(webpage, num_pages=1):
    """ Takes in the makaan.com URL and fetches the
    listings for the number of pages specified.
    Returns the list of json of all listings(includes ads).
    """
    listings = []
    json_list = []

    for i in range(1, num_pages + 1):
        # Url for the page
        url = webpage.split('?')[0] + '?page=' + str(i)
        # fetching page and contents
        page = requests.get(url)
        content = BeautifulSoup(page.content, 'html.parser')
        # find list of listing - 21 listings per page
        house_data = content.find_all('li', class_="cardholder")
        listings.extend(list(house_data))

    for i in range(len(listings)):
        json_list.append(list(listings)[i].find_all('script', {"type": "text/x-config"})[0].text)
    return json_list


def remove_ads(list_json):
    """ Takes in the list of JSON and returns list of JSON without Adds.
    """
    clean_json = []

    # iterate over list of json

    for i in range(len(list_json)):
        temp = json.loads(list_json[i])
        key = list(temp.keys())[0]
        if key == 'selector':
            clean_json.append(temp)

    return clean_json


def json_to_df(list_json):
    """ Takes in the list of JSON and creates a Pandas DF.
    Returns DF with each listing as a row and the columns - 'id', 'size', 'propertyType',"bedrooms",
    'latitude', 'longitude', 'localityName', 'suburbName', 'cityName', 'price', 'companyName'
    """
    # create a dataframe
    data = pd.DataFrame(columns=['id', 'size', 'propertyType', "bedrooms",
                                 'latitude', 'longitude', 'localityName', 'suburbName', 'cityName', 'price',
                                 'companyName'])

    # iterate over JSON
    for i in range(len(list_json)):
        temp = list_json[i]
        try:
            data.loc[i] = [temp['id'], temp['size'], temp['propertyType'], temp['bedrooms'],
                           temp['latitude'], temp['longitude'], temp['localityName']
                , temp['suburbName'], temp['cityName'], temp['price'], temp['companyName']]
        except KeyError:
            pass

    return data


def listings_to_df(webpage, num_pages=1):
    """
    Takes in the makaan.com first page of results and evokes the other function to automatically return a cleaned
    Pandas DF. Offers less control but single function to get data.
    :return: DF with each listing as a row and the columns - 'id', 'size', 'propertyType',"bedrooms",
    'latitude', 'longitude', 'localityName', 'suburbName', 'cityName', 'price', 'companyName'.
    :example call: listings_df('https://www.makaan.com/delhi/delhi-east-flats-for-rent-10019?page=1', num_pages = 10)
    """
    temp_json = fetch_listings(webpage, num_pages)
    temp_clean_json = remove_ads(temp_json)
    data = json_to_df(temp_clean_json)

    return data
