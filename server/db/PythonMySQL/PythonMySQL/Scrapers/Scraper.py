import requests
import mysql.connector
from bs4 import BeautifulSoup
import sys


class Scraper:
    def __init__(self, webAddress):
        self.webAddress = webAddress

    #Basic connection
    def connectToWebsite(self):
        result = requests.get(self.webAddress)
        webDoc = BeautifulSoup(result.text, "html.parser")
        return webDoc

    #Connect To Database
    def connectToDatabase(self, hostInput, userNameInput, passwordInput, databaseInput):
        try:
            mydb = mysql.connector.connect(
                host=hostInput,
                user=userNameInput,
                password=passwordInput,
                db=databaseInput
        )
            if(mydb.is_connected):
                print("Connected To Database")
                return
        except:
            print("Connection Failed! Please check connection and try again")
            sys.exit()

    #The scraper also needs to send the data off to be cleaned! Or maybe it cleans the data itself?
    

class HouseScraper(Scraper):

    #Have a method for scavenging through the housing website and grabbing information
    #Have a method for cleaning it and then either uploading it to the database or saving it in lists/arrays/dicts/etc.
    pass

#Main
#Create Instance
HouseOne = HouseScraper("https://www.royallepage.ca/en/on/kingston/properties/")

#Method Testing
fileDoc = HouseOne.connectToWebsite()
HouseOne.connectToDatabase("localhost", "root", "123419Wimpa?", "testbase")