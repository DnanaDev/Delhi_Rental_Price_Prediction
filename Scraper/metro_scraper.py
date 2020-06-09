"""Delhi Metro Scraper
Fetches the Details(name, Line,Wiki pagelink,  layout, Coordinates) of each of the 229 New Delhi Metro
stations as of 9.6.20.
*Looses information about interchange stations. Only the first Line listed in table is saved.
5 Stations with no coordinates. [Dwarka sec 21, Hindon, Nangli, New Ashok Nagar, Najafgarh]
Extremely Slow, sends request to each stations individual wiki page to get coordinates.
 Works as of 9.6.20 *
"""

import requests
from bs4 import BeautifulSoup
import json


def get_coord(link):
    """Fetches Coordinates from the wiki pages of the stations. The pages in non-standard format are ignored
    and a 0,0 coord is returned. Add manually
    """
    try:
        station_source = requests.get(link)
        tomato_soup = BeautifulSoup(station_source.content, 'html.parser')
        coord = tomato_soup.findAll('span', class_='geo')[0].contents[0]
        lat = coord.split(';')[0]
        long = coord.split(';')[1].strip()
        return lat, long

    except IndexError:
        return 0.0, 0.0


# List of Metro Stations
source = requests.get(
    "http://en.wikipedia.org/wiki/List_of_Delhi_metro_stations",
    headers={'User-Agent': "Mozilla/5.0"})

print('*******Source read*********\n')

soup = BeautifulSoup(source.content, 'html.parser')
rows = soup.findAll('table')[1].findAll('tr')

lst = []

form = '{ "name": "%s",\
          "details": {"link":"%s",\
                      "line":"%s",\
                      "Layout":"%s",\
                      "latitude":%s,\
                      "longitude":%s }}'

# skipping first row of headers
for i, row in enumerate(rows[1:]):
    # Split rows for interchange stations in table
    # Probably a better way to deal with split rows than hard-coding the row.
    if i in [4, 10, 18, 21, 36, 46, 63, 70, 72, 83, 96, 99, 103, 104, 109, 113, 124, 129, 152, 155, 193, 195, 250, 252]:
        continue
    items = row.findAll('td')

    # Grabbing latitude and longitude from Station wiki page.
    link = "https://en.wikipedia.org" + items[0].findAll('a')[0].get('href')

    lat, long = get_coord(link)

    lst.append(form % (items[0].findAll('a')[0].contents[0],
                       link,
                       items[2].findAll('b')[0].contents[0],
                       items[4].contents[0],
                       float(lat),
                       float(long)))

string = r'[' + ','.join(lst) + ']'

# Removing new lines in the layout column for some entries.
string = string.replace("Elevated\n", "Elevated")
string = string.replace("Underground\n", "Underground")

data = json.loads(string)

f = open('metro.json', 'w+')
print('***Dumping metro.json****\n')
f.write(json.dumps(data, indent=4))
f.close()
