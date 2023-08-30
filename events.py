
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

collection = db['events']

# Make GET request to ARK Fandom
r = requests.get('https://ark.wiki.gg/wiki/Events')

# Parsing the HTML
doc = BeautifulSoup(r.content, 'html.parser')

# Base URL for images
BASE_IMG_URL = "https://ark.wiki.gg"

data = []

tables = doc.find_all(["table"], class_="wikitable")

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            continue
        else:
            img_src = BASE_IMG_URL + cols[0].find('img')["src"]
            cols = [ele.text.strip() for ele in cols]
            event = {
                "img_src": img_src,
                "eventName": cols[1],
                "startDate": cols[2],
                "endDate": cols[3],
            }
            data.append(event)
        
collection.insert_many(data)

client.close()