import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB 
from datetime import datetime
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
db_file = script_dir + "/" + "services.json"
db = TinyDB(db_file)
ITEM_KEY= 'item'

def addToDB(item):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    db.insert({ITEM_KEY:item, 'time':time})

def isEmptyDB():
    return db.__len__() == 0

def getLastDoc():
    el = db.all()[-1]
    record = db.get(doc_id=el.doc_id)
    return record

def allButLastIDs():
    lastDoc = getLastDoc()
    el_id = lastDoc.doc_id

    result = []
    for doc in db.all():
        if doc.doc_id == el_id:
            continue
        result.append(doc.doc_id)
    
    return result
    
def removeAllButLast():
    
    db.remove(doc_ids=allButLastIDs())
    
def compressDB():
    # TODO: use better algorithm to store history changes
    """
    removes all uneccessary data
    """
    removeAllButLast()

def shouldCompressDB():
    return db.__len__() > 100
    
def getLastStoredServices():
    record = getLastDoc()
    return record[ITEM_KEY]

def getServicesText():
    url = "https://www.bokadirekt.se/places/heda-ridklubb-12384"
    page = requests.get(url)
    s = BeautifulSoup(page.content, features="html.parser")
    rawServices = s.find(class_='services')
    return rawServices.text
        

def fetchServices() -> dict:
    result = {}
    url = "https://www.bokadirekt.se/places/heda-ridklubb-12384"
    page = requests.get(url)
    s = BeautifulSoup(page.content, features="html.parser")
    rawButtons = s.find(class_='services')
    
    if not rawButtons:
        return result
    
    rawServices = rawButtons.find_all('button', href=True)
    
    for rawService in rawServices:
        href = rawService['href']
        serviceId = int(href.split('-')[-1])
        title = rawService['title'].split("Boka ")[-1]
        result[serviceId] = title

    return result


def checkIsUpdatedServices():
    new = {'services': fetchServices(),
           'text': getServicesText()
           }
    isFirstCheck = isEmptyDB()
    if not isFirstCheck:
        prev = getLastStoredServices()

    # update db
    addToDB(new)
    new = getLastStoredServices()
    
    if shouldCompressDB():
        compressDB()
    
    if isFirstCheck:
        return False
        
    return new != prev
 
def main():
    s = fetchServices()
    print(s)
    s = checkIsUpdatedServices()
    print(s)
    

if __name__ == '__main__':
    main()
    
