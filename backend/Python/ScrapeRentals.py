#===================  Python with MongoDB for NoSQL databases  ==============

from pymongo import MongoClient
import requests #Connect To Webpage
from bs4 import BeautifulSoup
from pymongo.errors import DuplicateKeyError #Preventing duplicate entries

# -------- HOUSEKEEPING ---------- #
addresses = []
prices = []
typesOfProperty = []

# ------------ METHODS ------------ #

def addToMongo(lengthOfList, db):

    for i in range(0, lengthOfList):
        currentPrice = prices[i]
 
        valueToAdd = {
            "Address": addresses[i].strip(),
            "Property_Type": typesOfProperty[i].strip(),
            "Price": currentPrice
            }
        #--- Try to add to DB ---#
        # ---- THIS IS A LITTLE SLOW!! ---- #
        try:
            db.insert_one(valueToAdd)
            print("Value added at index ", i)
            #db.insert_many(documentToUpload)
        except DuplicateKeyError:
            print("Duplicate Not Added at Index: " + str(i))

def scrapeWebsiteSetup(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc
def scrapeAndSave(doc, addresses, prices, typesOfProperty):
        price = doc.find_all(class_="title--h3 price") #all prices
        propertyTypes = doc.find_all(class_="listing-meta listing-meta--small") #All Types
        address = doc.find_all(class_="address-1") #All addresses

        try:
            for i in range(0, 46):
                one = price[i].text #Single Price
                one = one.replace('\n', '')

                oneProperty = propertyTypes[i].text #One Type

                oneAddress = address[i].text #Single Address

                typesOfProperty.append(oneProperty) #Add Type
                addresses.append(oneAddress) #Add address
                prices.append(one) #Add Price

                outputOne = "First Page, listing #{}".format(i) + oneAddress
                print(outputOne)
        except:
            print("Out Of First Try!")
        #Iterate through each page and grab the data. Think of it like a 2D array!   
 
        for i in range(1, 13):
            pageNumber = "Page #{}".format(i)
            print(pageNumber)
            urlCount = "https://www.royallepage.ca/en/searchgeo/homes/on/kingston/{}/?search_str=Kingston%2C+Ontario%2C+CAN&csrfmiddlewaretoken=1ILvxH5iocu8VRzY6yBX59x0ljgJZuvdC82UEt4FZgb1KTg0UBp8GpD3QSNPb3j8&property_type=&house_type=&features=&listing_type=&lat=44.300222396850586&lng=-76.4619255065918&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=&travel_time_min=&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=None&address=Kingston&method=homes&address_type=city&city_name=Kingston&prov_code=ON&school_id=&boundary=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=LEASE&archive_timespan=3&keyword=&sortby=".format(i + 1)
            secondResult = requests.get(urlCount)
            secondDoc = BeautifulSoup(secondResult.text, "html.parser")

            try:
                price = secondDoc.find_all(class_="title--h3 price") #Find all prices
                address = secondDoc.find_all(class_="address-1") #Find all addresses
                propertyTypes = secondDoc.find_all(class_="listing-meta listing-meta--small") #Find all Types

                for i in range(0, 46):
                    one = price[i].text #Single Price
                    one = one.replace('\n', '')

                    oneAddress = address[i].text #One address

                    oneProperty = propertyTypes[i].text #One Type

                    listingNumber = "Listing #{}".format(i) + oneAddress
                    print(listingNumber)
                    typesOfProperty.append(oneProperty) #Add Type
                    addresses.append(oneAddress) #Add address
                    prices.append(one) #Add Price
            except:
                print("Out Of Try")
        for i in addresses:
            print(i)
# ----------- CLASS SETUP ----------#

url = "https://www.royallepage.ca/en/searchgeo/homes/on/kingston/?search_str=Kingston%2C+Ontario%2C+CAN&csrfmiddlewaretoken=1ILvxH5iocu8VRzY6yBX59x0ljgJZuvdC82UEt4FZgb1KTg0UBp8GpD3QSNPb3j8&property_type=&house_type=&features=&listing_type=&lat=44.300222396850586&lng=-76.4619255065918&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=&travel_time_min=&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=None&address=Kingston&method=homes&address_type=city&city_name=Kingston&prov_code=ON&school_id=&boundary=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=LEASE&archive_timespan=3&keyword=&sortby="
doc = scrapeWebsiteSetup(url) # ---- Connect To Website ---- #
scrapeAndSave(doc, addresses, prices, typesOfProperty)

# --------- Connect To DB -------- #
    
client = MongoClient("mongodb+srv://JayMills:123419Wimpa@housingcluster.otlewh3.mongodb.net/")
db = client.KingstonHouses #Refer to DB. If non existant, one is created
houses = db.Rentals #Refer to collections. Same as above

# ------- Try to make a unique address index ---------- #
try:
    houses.create_index("Address", unique=True)
except:
    pass

lengthOfList = len(addresses)

addToMongo(lengthOfList, houses)

# --------- TODO ----------#

#Add Realtor.ca to the list and see if it will work using less requests. ie: 1 request per page


# =========== REALTOR Has bot protection... ============#
