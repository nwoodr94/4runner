#!./bin/python3.7

import urllib
from selenium.webdriver import Chrome 
from bs4 import BeautifulSoup
import pandas as pd

# Build query parameters
params = urllib.parse.urlencode(
    {
        'bundle_duplicates': 1, # Yes Bundle
        'search_distance': 180, # Miles from Postal
        'postal': 90640, # Current Location
        'auto_make_model': 'toyota+4runner',
        'min_auto_year': 2003,
        'max_auto_year': 2009,
        'auto_drivetrain': 3, # 4WD
        'auto_title_status': 1 # Clean
    }
)

url = "https://losangeles.craigslist.org/search/cto?%s" %params

# Initialize Selenium WebDriver for Chrome and navigate to URL
driver = Chrome(executable_path='./bin/chromedriver')
driver.get(url)

# Turn HTML source code into soup
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')


# Get 4Runner links, date posted, price, distance, and uid
link, date, price, distance, uid = [], [], [], [], []

for result in soup.find_all('p', attrs={'class': 'result-info'}):
    link += [result.find('a').get('href')]

for result in soup.find_all('time', attrs={'class': 'result-date'}):
    date += [result.get_text()]

for result in soup.find_all('span', attrs={'class': 'result-price'}):
    # Filter duplicates
    if(result.parent.name == 'a'):
        price += [result.get_text()]

for result in soup.find_all('span', attrs={'class': 'maptag'}):
    distance += [result.get_text()]

for result in soup.find_all('li', attrs={'class': 'result-row'}):
    uid += [result.get('data-pid')]



# Iterate through each listing, and append each property to a list of attributes
runners = {}
for runner in range(len(link)):
    attribute_list = [date[runner], price[runner], distance[runner]]

    driver.get(link[runner])
    listing = driver.page_source
    soup = BeautifulSoup(listing, 'html.parser')

    # There are at most 2 attribute groups containing useful span elements 
    for group in soup.find_all('p', attrs={'class': 'attrgroup'}, limit=2):
        for span in group.find_all('span'):
            prop = span.text
            attribute_list += [prop]
        
    attribute_list += [link[runner], uid[runner]]
    
    # Each listing is an index in the runners dictionary
    runners[runner] = attribute_list


# Write listings into a deliverable in /dist
with open("./dist/listings.txt", "w+") as f: 
    for i in runners:
        f.write('\n'.join(runners[i])+'\n\n')
    f.close()