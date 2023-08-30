
'''
This code was created by Jacob Cuison
Purpose is to scrape information from ARK Fandom and store into a MySQL Database and exposed using ARK Api
'''

import requests
from bs4 import BeautifulSoup

# Package to connect to MongoDB
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

# Loading environment files from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

DB_NAME = os.getenv('DB_NAME')

# Connect to database based using environment variables
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))

db = client[DB_NAME]

collection = db['resources']

# Make GET request to ARK Fandom
r = requests.get('https://ark.wiki.gg/wiki/Resources')

# Parsing the HTML
doc = BeautifulSoup(r.content, 'html.parser')
data = []

resourceTable = doc.find(['table'], class_='wikitable')
resourceTableBody = resourceTable.tbody
resourceTableRows = resourceTableBody.find_all('tr')

for resourceRow in resourceTableRows:
    
    resourceData = resourceRow.find_all('td')
    # print(resourceRow)

    if len(resourceData) == 0:
        continue
    else:
        resourceProperties = []

        for cell in resourceData:
            img = cell.find('img')
            if img:
                if img['alt'] == 'Check mark.svg':
                    img_alt = True
                elif img['alt'] == 'X mark.svg':
                    img_alt = False
                else:
                    img_alt = "N/A"
                resourceProperties.append(img_alt)

        resourceData = [ele.text.strip() for ele in resourceData]

        newResource = {
            "Item": resourceData[0],
            "Rarity": resourceData[1],
            "Properties": {
                "Renewable": resourceProperties[1],
                "Refinable": resourceProperties[2],
                "Combustible": resourceProperties[3]
            }
        }

        data.append(newResource)
        
collection.insert_many(data)

client.close()