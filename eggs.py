
'''
This code was created by Jacob Cuison
Purpose is to scrape information from ARK Fandom and store into a MySQL Database and exposed using ARK Api
'''

import requests
from bs4 import BeautifulSoup

# Package to connect to MongoDB
from pymongo import MongoClient

import os
from dotenv import load_dotenv

# Loading environment files from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

DB_NAME = os.getenv('DB_NAME')

# Connect to database based using environment variables
client = MongoClient(os.getenv('MONGODB_URI'))

db = client[DB_NAME]

collection = db['eggs']

# Make GET request to ARK Fandom
r = requests.get('https://ark.fandom.com/wiki/Eggs')

# Parsing the HTML
doc = BeautifulSoup(r.content, 'html.parser')

eggData = []
newEgg = {}
eggs = []

eggTable = doc.find(['table'], class_='wikitable')

for index, row in enumerate(eggTable.find_all('tr')):
    # print(str(index))
    rowHeader = row.find('th')
    if rowHeader and 'colspan' in rowHeader.attrs and rowHeader['colspan'] == '3' and index != 1:
        newEgg['eggs'] = eggs
        eggs = []
        eggData.append(newEgg)
        newEgg = {}
        newEgg['eggType'] = rowHeader.get_text(strip=True)
        # print('<th> found at index ' + str(index))
        # print(rowHeader)
    elif rowHeader and index == 1:
        newEgg['eggType'] = rowHeader.get_text(strip=True)

    rowData = row.find_all('td')
    
    for currentRow in rowData:
        if 'rowspan' in currentRow.attrs:
            ul = currentRow.find('ul')
            if ul:
                favoredByList = []
                for li in ul.find_all('li'):
                    favoredByList.append(li.text.strip())
                newEgg['favoredBy'] = favoredByList
            else:
                kibble = currentRow.get_text(strip=True)
                newEgg['kibble'] = kibble
        else:
            eggs.append(currentRow.get_text(strip=True))
    

# print(eggData)

collection.insert_many(eggData)

client.close()
