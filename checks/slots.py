import requests
from checks.exceptions import ParseException, FetchException
from checks.services import fetchServices
import sys
import traceback
from datetime import datetime

DEBUG = True

def calcTicks():
    """
    bokadirekt uses their own time measurement. 
    Check this function if time interval is inaccurate
    """
    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    baseDate, baseTicks = ("2022-08-21T1:00:00", 1661040000000)
    baseTime = datetime.strptime(baseDate, TIME_FORMAT)
    now = datetime.today()
    delta = now-baseTime
    days = int(delta.total_seconds()/(3600*24))
    weeks = int(days/7)
    
    ticksPerWeek =  760400000 # ticks for a week
    ticks = baseTicks + weeks * ticksPerWeek

    return ticks

def getUrl(serviceId):
    ticks = calcTicks()
    url = f"https://www.bokadirekt.se/api/book/{(serviceId)}/12384/{ticks}/10650?reborn=true"
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
    services = fetchServices()
    availableSlots = []
    for serviceTitle, serviceId in services.items():
        if DEBUG: print(f" - Fetching service: '{serviceTitle}' with ID: '{serviceId}'")
        availableSlots += fetchSlotsByService(serviceId)
    
    return availableSlots

def main():
    s = fetchSlots()
    print(s)

if __name__ == '__main__':
    main()
    