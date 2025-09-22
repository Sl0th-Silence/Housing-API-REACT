from bs4 import BeautifulSoup
import requests
import mysql.connector


#HK
host = "localhost"
userName = "root"
password = "123419Wimpa?"
database = "housingprices"

url = "https://www.royallepage.ca/en/on/kingston/properties/"

addresses = []
prices = []
typesOfProperty = []
priceRangeTags = ['0 - 300,000', '300,001 - 600,000', '600,001 - 999,999', '1,000,000+']

#Database Connect
def databaseConnect(hostInput, userNameInput, passwordInput, databaseInput):
    mydb = mysql.connector.connect(
        host=hostInput,
        user=userNameInput,
        password=passwordInput,
        db=databaseInput
    )
    return mydb

mydb = databaseConnect(host, userName, password, database)
mycursor = mydb.cursor()

def scrapeWebsiteSetup(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc

doc = scrapeWebsiteSetup(url)

def scrapeSave(doc, addresses, prices, typesOfProperty):
    
    
    try:
        price = doc.find_all(class_="title--h3 price") #all prices
        propertyTypes = doc.find_all(class_="listing-meta listing-meta--small") #All Types
        address = doc.find_all(class_="address-1") #All addresses
        
        for i in range(0, 46):

            one = price[i].text #Single Price
            one = one.replace('$', '')
            one = one.replace(',', '')

            oneProperty = propertyTypes[i].text #One Type
            oneAddress = address[i].text #Single Address
            typesOfProperty.append(oneProperty) #Add Type
            addresses.append(oneAddress) #Add address
            prices.append(one) #Add Price

            outputOne = "First Page, listing #{}".format(i)
            print(outputOne)
    except:
        print("Out Of First Try!")
    #Iterate through each page and grab the data. Think of it like a 2D array!   
 
    for i in range(1, 13):
        pageNumber = "Page #{}".format(i)
        print(pageNumber)
        urlCount = "https://www.royallepage.ca/en/on/kingston/properties/{}/".format(i + 1)
        secondResult = requests.get(urlCount)
        secondDoc = BeautifulSoup(secondResult.text, "html.parser")

        try:
            price = secondDoc.find_all(class_="title--h3 price")
            address = secondDoc.find_all(class_="address-1")
            propertyTypes = secondDoc.find_all(class_="listing-meta listing-meta--small") #All Types

            for i in range(0, 46):
                listingNumber = "Listing #{}".format(i)
                print(listingNumber)
                one = price[i].text
                one = one.replace('$', '')
                one = one.replace(',', '')

                oneAddress = address[i].text

                oneProperty = propertyTypes[i].text #One Type

                typesOfProperty.append(oneProperty) #Add Type
                addresses.append(oneAddress)
                prices.append(one)
        except:
            print("Out Of Try")
    #TODO 
    #1. Connect/Create database
    #2. Check if database contains the data
    #3. Add data to database or update if price has changed
    #4.

scrapeSave(doc, addresses, prices, typesOfProperty)
tempTag = priceRangeTags[0]
lengthOfList = len(addresses)

for i in range(1, lengthOfList):
    if(int(prices[i]) <= 300000):
        tempTag = priceRangeTags[0]
    elif(int(prices[i]) > 300000 and int(prices[i]) < 600000):
        tempTag = priceRangeTags[1]
    elif(int(prices[i]) > 600000 and int(prices[i]) < 1000000):
        tempTag = priceRangeTags[2]
    else:
        tempTag = priceRangeTags[3]
    try:
        sql = "INSERT INTO HousesForSaleKingston_2025_06_16 (address, houseType, price, tag) VALUES (%s, %s, %s, %s)"
        values = (addresses[i], typesOfProperty[i], int(prices[i]), tempTag)
        mycursor.execute(sql, values)
    except:
        print("Can not add duplicate value at ", i)
mydb.commit()