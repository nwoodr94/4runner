#!./bin/python3.7

import urllib
from selenium.webdriver import Chrome 
from bs4 import BeautifulSoup
import pandas as pd

params = urllib.parse.urlencode(
    {
        'bundle_duplicates': 1, # Yes
        'search_distance': 100, # Miles from Postal
        'postal': 90640, 
        'auto_make_model': 'toyota+4runner',
        'min_auto_year': 2003,
        'max_auto_year': 2009,
        'auto_drivetrain': 3, # 4WD
        'auto_title_status': 1 # Clean
    }
)

url = "https://losangeles.craigslist.org/search/cto?%s" %params


driver = Chrome(executable_path='./bin/chromedriver')
driver.get(url)

elements = driver.find_elements_by_class_name('result-row')
result_count = len(elements)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

links = []
for result in soup.find_all('p', attrs={'class': 'result-info'}):
    links += [result.find('a').get('href')]

print(links)