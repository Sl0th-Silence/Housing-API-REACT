#===================  Python with MongoDB for NoSQL databases  ==============

from pymongo import MongoClient
import requests #Connect To Webpage
from bs4 import BeautifulSoup
from pymongo.errors import DuplicateKeyError #Preventing duplicate entries
from tqdm import tqdm # Progress bar
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

# ------------ METHODS ------------ #

def addToMongo(tempTag, lengthOfList, db):
    for i in tqdm(range(0, lengthOfList)):
        currentPrice = int(prices[i])
        
        if(currentPrice <= 300000):
            tempTag = priceRangeTags[0]
        elif(currentPrice > 300000 and int(prices[i]) < 600000):
            tempTag = priceRangeTags[1]
        elif(currentPrice > 600000 and int(prices[i]) < 1000000):
            tempTag = priceRangeTags[2]
        else:
            tempTag = priceRangeTags[3]
    
        
        valueToAdd = {
            "Address": addresses[i].strip(),
            "Property_Type": typesOfProperty[i].strip(),
            "Price": currentPrice,
            "Price_Range": tempTag
            }
        try:
            valueToAdd["Img_Link"] = imgLinks[i]
        except:
            print("No image link available / Out of scope")
            pass
        #--- Try to add to DB ---#
        try:
            db.insert_one(valueToAdd)
        except DuplicateKeyError:
            pass

def scrapeWebsiteSetup(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc

def scrapeAndSave(doc, addresses, prices, typesOfProperty, imgLinks):
        price = doc.find_all(class_="title--h3 price") #all prices
        propertyTypes = doc.find_all(class_="listing-meta listing-meta--small") #All Types
        address = doc.find_all(class_="address-1") #All addresses
        imgs = doc.find_all(class_="b-lazy")     
        for data in imgs:
            src = data.get("data-src") or data.get("src")
            imgLinks.append(src)
            print(src)
        try:
            for i in range(0, 46):
                one = price[i].text #Single Price
                one = one.replace('$', '')
                one = one.replace(',', '')

                oneProperty = propertyTypes[i].text #One Type
                oneAddress = address[i].text #Single Address

                typesOfProperty.append(oneProperty) #Add Type
                addresses.append(oneAddress) #Add address
                prices.append(one) #Add Price
        except:
            print("Something failed")
            pass
        #Iterate through each page and grab the data. Think of it like a 2D array!   
        print("Searching pages")
        for i in tqdm(range(1, 13)):
            urlCount = "https://www.royallepage.ca/en/on/kingston/properties/{}/".format(i + 1)
            secondResult = requests.get(urlCount)
            secondDoc = BeautifulSoup(secondResult.text, "html.parser")
            imgs = secondDoc.find_all(class_="b-lazy")
            print("Right before img loop")
            for img in imgs:
                src = img.get("data-src") or img.get("src")
                imgLinks.append(src)
                print(src)
            try:
                price = secondDoc.find_all(class_="title--h3 price") #Find all prices
                address = secondDoc.find_all(class_="address-1") #Find all addresses
                propertyTypes = secondDoc.find_all(class_="listing-meta listing-meta--small") #Find all Types
                for i in range(0, 46):
                    one = price[i].text
                    one = one.replace('$', '')
                    one = one.replace(',', '')

                    oneAddress = address[i].text #One address
                    oneProperty = propertyTypes[i].text #One Type

                    typesOfProperty.append(oneProperty) #Add Type
                    addresses.append(oneAddress) #Add address
                    prices.append(one) #Add Price
            except:
                pass
# ----------- BASIC SETUP ----------#

url = "https://www.royallepage.ca/en/on/kingston/properties/"
doc = scrapeWebsiteSetup(url) # ---- Connect To Website ---- #
scrapeAndSave(doc, addresses, prices, typesOfProperty, imgLinks)

# --------- Connect To DB -------- #
    
client = MongoClient(mongoURI)
db = client.KingstonHouses #Refer to DB. If non existant, one is created
houses = db.Houses_One #Refer to collections. Same as above

# ------- Try to make a unique address index ---------- #
try:
    houses.create_index("Address", unique=True)
except:
    pass

tempTag = priceRangeTags[0]
lengthOfList = len(addresses)

addToMongo(tempTag, lengthOfList, houses)

# --------- TODO ----------#

#Add Realtor.ca to the list and see if it will work using less requests. ie: 1 request per page


# =========== REALTOR Has bot protection... ============#
