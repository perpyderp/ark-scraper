
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

collection = db['armor']

# Make GET request to ARK Fandom
r = requests.get('https://ark.fandom.com/wiki/Armor')

# Parsing the HTML
doc = BeautifulSoup(r.content, 'html.parser')

armorData = []
data = []

armorTable = doc.find(['table'], class_='wikitable')
amorTableBody = armorTable.tbody
armorTableRows = amorTableBody.find_all('tr')

for armorRow in armorTableRows:
    
    armorData = armorRow.find_all('td')

    if len(armorData) == 0:
        continue
    else:
        armorLink = "https://ark.fandom.com" + armorRow.find('a').get('href')
        armorData = [ele.text.strip() for ele in armorData]

        newArmor = {
            "armor_type": armorData[0],
            "unlock_level": armorData[1], 
            "armor_rating": armorData[2], 
            "cold_protection": armorData[3],
            "heat_protection": armorData[4],
            "weight": armorData[5],
            "durability": armorData[6],
            "found_in": armorData[7],
            "ingredients": armorData[8],
            "url": armorLink
        }

        data.append(newArmor)


collection.insert_many(data)
