import requests #Connect To Webpage
from bs4 import BeautifulSoup
from pymongo.errors import DuplicateKeyError #Preventing duplicate entries
from tqdm import tqdm # Progress bar


class WebScraperBase:
    def __init__(self, addresses, prices, typesOfProperty, imgLinks, priceRangeTags, url):
        self.addresses = addresses
        self.prices = prices
        self.typesOfProperty = typesOfProperty
        self.imgLinks = imgLinks
        self.priceRangeTags = priceRangeTags
        self.url = url

    #Methods
    #Website setup
    def scrapeWebsiteSetup(self, url):
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        return doc

    #Scrape and save information
    def scrapeAndSave(self, doc):
            price = doc.find_all(class_="title--h3 price") #all prices
            propertyTypes = doc.find_all(class_="listing-meta listing-meta--small") #All Types
            address = doc.find_all(class_="address-1") #All addresses
            imgs = doc.find_all(class_="b-lazy")     
            for data in imgs:
                src = data.get("data-src") or data.get("src")
                self.imgLinks.append(src)
                print(src)
            ctr = 0 #counter
            while(ctr < min(len(price), len(propertyTypes), len(address))): #while the counter is less than the smallest list, ie, not at the end, keep going
                try:        
                    one = price[ctr].text #Single Price
                    one = one.replace('$', '')
                    one = one.replace(',', '')

                    oneProperty = propertyTypes[ctr].text #One Type
                    oneAddress = address[ctr].text #Single Address

                    self.typesOfProperty.append(oneProperty) #Add Type
                    self.addresses.append(oneAddress) #Add address
                    self.prices.append(one) #Add Price
                    print("Going through first page: " + ctr)
                except:
                    print("Something failed")
                    pass
                finally:
                    ctr+= 1
            #Iterate through each page and grab the data. Think of it like a 2D array!

            print("Searching pages")
            urlIndex = 1

            while(len(imgs) != 0):
                urlCount = "https://www.royallepage.ca/en/on/kingston/properties/{}/".format(urlIndex + 1)
                secondResult = requests.get(urlCount)
                secondDoc = BeautifulSoup(secondResult.text, "html.parser")
                imgs = secondDoc.find_all(class_="b-lazy")
                
                print("Page: " + str(urlIndex))
                for img in imgs:
                    src = img.get("data-src") or img.get("src")
                    self.imgLinks.append(src)
                    print(src)
                urlIndex+= 1
                ctr = 0 #counter
                while(ctr < min(len(price), len(propertyTypes), len(address))):
                    try:
                        price = secondDoc.find_all(class_="title--h3 price") #Find all prices
                        address = secondDoc.find_all(class_="address-1") #Find all addresses
                        propertyTypes = secondDoc.find_all(class_="listing-meta listing-meta--small") #Find all Types
                        one = price[ctr].text
                        one = one.replace('$', '')
                        one = one.replace(',', '')

                        oneAddress = address[ctr].text #One address
                        oneProperty = propertyTypes[ctr].text #One Type

                        self.typesOfProperty.append(oneProperty) #Add Type
                        self.addresses.append(oneAddress) #Add address
                        self.prices.append(one) #Add Price
                    except:
                        pass
                    finally:
                        print("Entry: " + str(ctr))
                        ctr+= 1

    #Add information to mongodb
    def addToMongo(self, tempTag, db):
        for i in tqdm(range(0, len(self.addresses))):
            currentPrice = int(self.prices[i])
            
            if(currentPrice <= 300000):
                tempTag = self.priceRangeTags[0]
            elif(currentPrice > 300000 and int(self.prices[i]) < 600000):
                tempTag = self.priceRangeTags[1]
            elif(currentPrice > 600000 and int(self.prices[i]) < 1000000):
                tempTag = self.priceRangeTags[2]
            else:
                tempTag = self.priceRangeTags[3]
        
            
            valueToAdd = {
                "Address": self.addresses[i].strip(),
                "Property_Type": self.typesOfProperty[i].strip(),
                "Price": currentPrice,
                "Price_Range": tempTag
                }
            try:
                valueToAdd["Img_Link"] = self.imgLinks[i]
            except:
                print("No image link available / Out of scope")
                pass
            #--- Try to add to DB ---#
            try:
                db.insert_one(valueToAdd)
            except DuplicateKeyError:
                pass