import requests
from condition.exceptions import ParseException, FetchException
import sys
import traceback

services = {
    "Stallag fodervärd": 106767, 
    "Stallag privat - morgon och lunch" : 106768, 
    "Stallag privat - insläpp och kväll" : 106769, 
    "kvällsfodring privat": 106770,
    "Morgon fodring privat, sommar" : 600770,
    "Em fodring, sommar" : 106764,
    "Lunchfodring, sommar" : 600769,
}

def getUrl(serviceId):
    url = f"https://www.bokadirekt.se/api/book/{(serviceId)}/12384/1670288400000/10650?reborn=true"
    return url
    
def getJson(serviceId):
    url = getUrl(serviceId)
    try:
        response = requests.get(url)
        return response.json()

    except Exception:
        exc_type, value, tb = sys.exc_info()
        raise FetchException(str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))

def parse(data):
    try:
        return data["availability"]["fromErpOverview"]["datesWithOpeningHours"]
    except Exception:
        exc_type, value, tb = sys.exc_info()
        raise ParseException(str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))


def fetchSlotsByService(serviceId):
    data = getJson(serviceId)
    return parse(data)

def fetchSlots():
    availableSlots = []
    for service in services.values():
        availableSlots += fetchSlotsByService(service)
    
    return availableSlots

def main():
    s = fetchSlots()
    print(s)

if __name__ == '__main__':
    main()
    