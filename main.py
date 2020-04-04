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

# Get 4Runner links, date posted, price, and distance from zip
links = []
dates = []
prices = []
distances = []

for result in soup.find_all('p', attrs={'class': 'result-info'}):
    links += [result.find('a').get('href')]

for result in soup.find_all('time', attrs={'class': 'result-date'}):
    dates += [result.get_text()]

for result in soup.find_all('span', attrs={'class': 'result-price'}):
    prices += [result.get_text()]

for result in soup.find_all('span', attrs={'class': 'maptag'}):
    distances += [result.get_text()]

# Iterate through each listing, and append each property to a list of attributes
runners = {}
for runner in range(len(links)):
    attribute_list = [dates[runner], prices[runner], distances[runner]]

    # Listing details are available only on its respective source code
    driver.get(links[runner])
    listing = driver.page_source
    soup = BeautifulSoup(listing, 'html.parser')

    #There are two attribute groups containing useful span elements 
    for group in soup.find_all('p', attrs={'class': 'attrgroup'}):
        for span in group.find_all('span'):
            prop = span.text
            attribute_list += [prop]
        
    attribute_list += [links[runner]]
    
    # Each listing is an index in the runners dictionary
    runners[runner] = attribute_list

print(runners[0])
# ['Mar 19', '$4900', '15.9mi', '2005 toyota 4runner', 'condition: good', 'cylinders: 6 cylinders', 'drive: 4wd', 'fuel: gas', 'title status: clean', 'transmission: automatic', 'https://losangeles.craigslist.org/wst/cto/d/carson-2005-toyota-4runner-sr5-4x4/70959']