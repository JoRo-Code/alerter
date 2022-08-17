import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB 
from datetime import datetime
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
db_file = script_dir + "/" + "services.json"
db = TinyDB(db_file)
SERVICES_KEY = 'services'

def addToDB(item):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    db.insert({SERVICES_KEY:item, 'time':time})

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
    
        

def fetchServices():
    url = "https://www.bokadirekt.se/places/heda-ridklubb-12384"
    page = requests.get(url)
    s = BeautifulSoup(page.content, features="html.parser")
    services = s.find(class_='services').find_all(class_='item')
    
    result = []
    for service in services:
        parsedService = service.text.split("·")[0]
        result.append(parsedService)

    return result

def getLastStoredServices():
    record = getLastDoc()
    return record[SERVICES_KEY]

def checkIsUpdatedServices():
    new = fetchServices()
    isFirstCheck = isEmptyDB()
    if not isFirstCheck:
        prev = getLastStoredServices()

    # update db
    addToDB(new)
    
    if shouldCompressDB():
        compressDB()
    
    if isFirstCheck:
        return False
        
    return new != prev

        
 
def main():
    s = checkIsUpdatedServices()
    print(s)

if __name__ == '__main__':
    main()
    
