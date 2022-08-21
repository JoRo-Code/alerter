import requests
from exceptions import ParseException, FetchException
import sys
import traceback
import random

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
    sessionId = str(random.randint(1000000,9999999))+"00000"

    url = f"https://www.bokadirekt.se/api/book/{(serviceId)}/12384/{sessionId}/10650?reborn=true"
    return url
    
def getJson(serviceId):
    url = getUrl(serviceId)
    try:
        response = requests.get(url)

    except Exception:
        exc_type, value, tb = sys.exc_info()
        raise FetchException("Error: Couldn't fetch URL. Traceback: "+ str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))
    else:
        try:
            json = response.json()
        except Exception:
            exc_type, value, tb = sys.exc_info()
            raise ParseException("Error: Couldn't parse response. " + "Response: " + str(response.content) + " Traceback: " + str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))
        else:
            return json
        


def parse(data, serviceId):
    try:
        result = data["availability"]["fromErpOverview"]["datesWithOpeningHours"]
    except Exception:
        exc_type, value, tb = sys.exc_info()
        raise ParseException(str(serviceId) + ": " + str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))
    else:
        return result


def fetchSlotsByService(serviceId):
    data = getJson(serviceId)
    return parse(data, serviceId)

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
    