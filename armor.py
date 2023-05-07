
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

# Regular expression package
import re

def parse_ingredients(string):
    ingredients = []
    pattern = r'(\d+)\s*[×x]\s*([A-Za-z]+)'
    matches = re.findall(pattern, string)
    for match in matches:
        quantity = int(match[0])
        material = match[1].strip()
        ingredient = {'quantity': quantity, 'material': material}
        ingredients.append(ingredient)
    return ingredients


# Loading environment files from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

DB_NAME = os.getenv('DB_NAME')

# Connect to database based using environment variables
client = MongoClient(os.getenv('MONGODB_URI'))

db = client[DB_NAME]

collection = db['armors']

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
            "armorType": armorData[0],
            "unlockLevel": armorData[1], 
            "armorRating": armorData[2], 
            "coldProtection": armorData[3],
            "heatProtection": armorData[4],
            "weight": armorData[5],
            "durability": armorData[6],
            "foundIn": armorData[7],
            "ingredients": parse_ingredients(armorData[8]),
            "url": armorLink
        }

        data.append(newArmor)

collection.insert_many(data)

client.close()