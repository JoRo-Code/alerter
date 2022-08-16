import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB
from datetime import datetime

db = TinyDB('services.json')
SERVICES_KEY = 'services'

def addToDB(item):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    db.insert({SERVICES_KEY:item, 'time':time})

def isEmptyDB():
    return len(db.all()) == 0

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
    el = db.all()[-1]
    record = db.get(doc_id=el.doc_id)
    return record[SERVICES_KEY]

def checkIsUpdatedServices():
    new = fetchServices()
    isFirstCheck = isEmptyDB()
    if not isFirstCheck:
        prev = getLastStoredServices()

    # update db
    addToDB(new)
    
    if isFirstCheck:
        return False
        
    return new != prev
 
def main():
    s = checkIsUpdatedServices()
    print(s)

if __name__ == '__main__':
    main()
    