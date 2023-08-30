
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

collection = db['status_effects']

# Make GET request to ARK Fandom
r = requests.get('https://ark.wiki.gg/wiki/Status_effects')

# Parsing the HTML
doc = BeautifulSoup(r.content, 'html.parser')
data = []

tables = doc.find_all(['table'], class_='status-effect-backg')

BASE_IMG_URL = "https://ark.wiki.gg/"

for table in tables:

    newStatus = {
        "name": "",
        "message": "",
        "HUD_Text": "",
        "information": "",
        "note": [],
        "img_src": []
    }
    tableRows = table.find_all('tr')
    name = tableRows[0].find('b').get_text()
    if(name == ""):
        newStatus["name"] = "N/A"
    else:
        newStatus["name"] = name

    img_src = tableRows[1].find_all("img")
    for i in range(len(img_src)):
        newStatus["img_src"].append(BASE_IMG_URL + img_src[i]["src"])

    status_description = tableRows[1].find_all("p")
    for i in range(len(status_description)):
        desc_category = status_description[i].text
        # print("Description category: " + desc_category)
        if(desc_category.find("Message") != -1):
            # print("Found message: " + desc_category)
            newStatus["message"] = desc_category
        elif(desc_category.find("HUD Text") != -1):
            # print("Found HUD Text: " + desc_category)
            newStatus["HUD_Text"] = desc_category
        elif(desc_category.find("Information") != -1):
            # print("Found information: " + desc_category)
            newStatus["information"] = desc_category
        elif(desc_category.find("Note") != -1):
            # print("Found note: " + desc_category)
            for(j, note) in enumerate(tableRows[1].find_all("li")):
                newStatus["note"].append(note.text)

    # print(newStatus)

    data.append(newStatus)
        
collection.insert_many(data)

client.close()