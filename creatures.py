
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

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
CLUSTER = os.getenv('CLUSTER_NAME')

# Connect to database based using environment variables


client = MongoClient("mongodb+srv://" + USER + ":" + PASSWORD + "@" + CLUSTER + ".mongodb.net/" + DB_NAME + "?retryWrites=true&w=majority")

db = client[DB_NAME]

collection = db['creatures']

# Make GET request to ARK Fandom
r = requests.get('https://ark.fandom.com/wiki/Creatures')

# Parsing the HTML
doc = BeautifulSoup(r.content, 'html.parser')

creatureData = []
data = []

creatureTable = doc.find(['table'], class_='cargo-creature-table')
creatureTableBody = creatureTable.tbody
creatureTableRows = creatureTableBody.find_all('tr')

for creatureRow in creatureTableRows:
    
    creatureData = creatureRow.find_all('td')

    if len(creatureData) == 0:
        continue
    else:
        creatureLink = "https://ark.fandom.com" + creatureRow.find('a').get('href')

        creatureData = [ele.text.strip() for ele in creatureData]

        newCreature = {
            'name': creatureData[0], 
            'diet': creatureData[2], 
            'temperament': creatureData[3], 
            'tameable': creatureData[4], 
            'rideable': creatureData[5], 
            'breedable': creatureData[6], 
            'saddleLevelObtained': creatureData[7], 
            'creatureID': creatureData[8], 
            'url': creatureLink
        }

        data.append(newCreature)


collection.insert_many(data)
