from pymongo import MongoClient
import re
from pymongo.errors import DuplicateKeyError
import os
from dotenv import load_dotenv

#dot env setup
load_dotenv()

mongoURI = os.getenv("MONGO_DBI")
# -- Open Database -- #

client = MongoClient(mongoURI)
db = client.KingstonHouses #Refer to DB. If non existant, one is created
houses = db.Rentals #Refer to collections. Same as above

def clean_whitespace(value): # -- Pulled from stack. New to re -- #
    if isinstance(value, str):
        # Remove leading/trailing whitespace and collapse multiple spaces/newlines
        return re.sub(r'\s+', ' ', value.strip())
    return value

def updateDatabase(houses):
    for house in houses.find():
        cleanedData = {}
        for each in ["Address", "Property_Type", "Price"]:
            cleaned = clean_whitespace(house.get(each))
            if cleaned != house.get(each):
                cleanedData[each] = cleaned
        if cleanedData:
            print(cleanedData)
            try:
                houses.update_one({"_id": house["_id"]}, {"$set": cleanedData})
                print("Updated", house["_id"], "with: ", cleanedData)
            except DuplicateKeyError:
                houses.delete_one(house)
                print("Dropped House for being a Duplicate")


def outputDataAddresses(houses):
    for house in houses.find():
        print(house["Address"])

updateDatabase(houses)
#outputDataAddresses(houses)