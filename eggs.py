
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
data = []

eggTable = doc.find(['table'], class_='wikitable')
eggTableHeader = eggTable.find_all('th')
eggTableBody = eggTable.tbody
eggTableRows = eggTableBody.find_all('tr')

print(eggTable)
# print(eggTableRows)

# for armorRow in armorTableRows:
    
#     armorData = armorRow.find_all('td')

#     if len(armorData) == 0:
#         continue
#     else:
#         armorLink = "https://ark.fandom.com" + armorRow.find('a').get('href')
#         armorData = [ele.text.strip() for ele in armorData]

#         newArmor = {
#             "armorType": armorData[0],
#             "unlockLevel": armorData[1], 
#             "armorRating": armorData[2], 
#             "coldProtection": armorData[3],
#             "heatProtection": armorData[4],
#             "weight": armorData[5],
#             "durability": armorData[6],
#             "foundIn": armorData[7],
#             "ingredients": parse_ingredients(armorData[8]),
#             "url": armorLink
#         }

#         data.append(newArmor)

# collection.insert_many(data)

# client.close()