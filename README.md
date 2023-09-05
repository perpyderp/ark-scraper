# ark-scraper

These python files can be used to scrape data from both
https://ark.fandom.com/wiki/ARK_Survival_Evolved_Wiki and https://ark.wiki.gg/wiki/ARK_Wiki

To these scrapers, you must initialize your environment variables either by creating a .env file or in your system environment variables.

This scraper utilizes MongoDB, however you can easily tweak the code for other DBs

The following variables must be initialized, or you can modify the code however you please.

DB_USER=<mongodb-username>
DB_PASSWORD<mongodb-password>
CLUSTER_NAME=<cluster-name>
DB_NAME=arkDB
SERVER_PORT=<server-port>
MONGODB_URI=<your-mongodb-uri>