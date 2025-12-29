#===================  Python with MongoDB for NoSQL databases  ==============
from ScraperClass import WebScraperBase #Import the class I made
from pymongo import MongoClient
import os
from dotenv import load_dotenv

#dot env setup
load_dotenv("C:\\Users\\Jay_M\\Desktop\\Summer Work\\Housing-API-REACT\\backend\\.env")

mongoURI = os.getenv("MONGO_DBI")

# -------- HOUSEKEEPING ---------- #
addresses = []
prices = []
typesOfProperty = []
imgLinks = []
priceRangeTags = ['0 - 300,000', '300,001 - 600,000', '600,001 - 999,999', '1,000,000+']

# ----------- INSTANTIATE ---------- #
url = "https://www.royallepage.ca/en/on/kingston/properties/"

kingstonHouse = WebScraperBase(addresses=addresses, 
                               prices=prices, 
                               typesOfProperty=typesOfProperty, 
                               imgLinks=imgLinks, 
                               priceRangeTags=priceRangeTags, 
                               url=url)

# ----------- BASIC SETUP ----------#
doc = kingstonHouse.scrapeWebsiteSetup(url=url) # ---- Connect To Website ---- #
kingstonHouse.scrapeAndSave(doc=doc)

# --------- Connect To DB -------- #
    
client = MongoClient(mongoURI)
db = client.KingstonHouses #Refer to DB. If non existant, one is created
houses = db.Houses_One #Refer to collections. Same as above

# ------- unique address index ---------- #
try:
    houses.create_index("Address", unique=True)
except:
    pass

tempTag = priceRangeTags[0]
lengthOfList = len(kingstonHouse.addresses)

kingstonHouse.addToMongo(tempTag=tempTag, db=houses)
