from matplotlib import pyplot as plt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# -- Load dotenv file
load_dotenv()

MongoURL = os.getenv("MONGO_URL")

client = MongoClient(MongoURL)
db = client.KingstonHouses #Refer to DB. If non-existent, one is created
houses = db.Houses_One #Refer to collections. Same as above
data = houses.find({})

numOfHouses = 0
types = []
prices = []
lowestPrice = 500000 # -- Set default value
lowestType = ""

highestPrice = 0
highestType = ""

for house in data:
    types.append(house['Property_Type'])
    prices.append(house['Price'])
    numOfHouses += 1

    # lowest price/type
    if lowestPrice > house['Price']:
        lowestPrice = house['Price']
        lowestType = house['Property_Type']

    # highest price/type
    if highestPrice < house['Price']:
        highestPrice = house['Price']
        highestType = house['Property_Type']


# --------- TODO ---------- #
# -- Sort all data by Price and Type. -- #
# -- Find the average, low and high -- #
# -- Display All the information -- #

averagePrice = sum(prices) / numOfHouses
averagePrice = ("{:.2f}".format(averagePrice))

print("Average Price: $" + str(averagePrice))

print("$" + str(lowestPrice) + ".00")
print("Type: " + lowestType)

print("$" + str(highestPrice) + ".00")
print("Type: " + highestType)

print("Number of houses: " + str(numOfHouses))