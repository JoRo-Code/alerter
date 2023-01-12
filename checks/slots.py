import requests
from checks.exceptions import ParseException, FetchException
from checks.services import fetchServices
from checks.ticks import getTodaysTicks
import sys
import traceback
from datetime import datetime
#from exceptions import ParseException, FetchException
#from services import fetchServices
#from ticks import getTodaysTicks

DEBUG = True
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

# placeholder for checked date
checkedStartDate = ""

def calcTicks():
    """
    bokadirekt uses their own time measurement. 
    Check this function if time interval is inaccurate
    """
    if DEBUG: print(f" - Fetching ticks")
    ticks = getTodaysTicks()

    return ticks

def getWeek(date:datetime) -> int:
    return date.isocalendar()[1]

def verifyCheckedPeriod(rawDate:str) -> Exception:
    """
    Checks if rawDate is corresponding to the current week
    """
    startDate = datetime.strptime(rawDate.split("+")[0], TIME_FORMAT)
    startWeek = getWeek(startDate)
    currentWeek = getWeek(datetime.now())
    
    #if DEBUG: print(f"   * Checked slots from: {startDate} (week {startWeek})")
    if startWeek != currentWeek:
        raise Exception(
            "WRONG SLOT PERIOD: Checked slot period is not corresponding to current week. " + 
            f"Check starting from week '{startWeek}' and not '{currentWeek}' ({startDate}). Check calcTicks-function.")
    
def getUrl(serviceId:int, ticks:int):
    url = f"https://www.bokadirekt.se/api/book/{(serviceId)}/12384/{ticks}/10650?reborn=true"
    return url
    
def getJson(serviceId:int, ticks:int):
    url = getUrl(serviceId, ticks)
    try:
        response = requests.get(url)

    except ConnectionError as e:
        if DEBUG: print("Found connection error while fetching url.")
        raise e
    except Exception:
        exc_type, value, tb = sys.exc_info()
        raise FetchException("Error: Couldn't fetch URL. Traceback: "+ str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))
    else:
        try:
            json = response.json()
        except ConnectionError as e:
            if DEBUG: print("Found connection error while parsing response: ")
            raise e
        except Exception:
            exc_type, value, tb = sys.exc_info()
            raise ParseException("Error: Couldn't parse response. " + "Response: " + str(response.content) + " Traceback: " + str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))
        else:
            return json
        


def parse(data, serviceId):
    try:
        overview = data["availability"]["fromErpOverview"]
        result = overview["datesWithOpeningHours"]
        
        
    except Exception:
        exc_type, value, tb = sys.exc_info()
        raise ParseException(str(serviceId) + ": " + str(exc_type.__name__) + ": " + str(value) + str(traceback.extract_tb(tb)))
    else:
        # verify checked week is correct
        global checkedStartDate 
        startDate = overview['minDateChecked']
        checkedStartDate = startDate
        
        verifyCheckedPeriod(startDate)
        
        return result


def fetchSlotsByService(serviceId:int, ticks:int):
    data = getJson(serviceId, ticks)
    return parse(data, serviceId)

def fetchSlots(serviceIDS:list[int] = None) -> dict:
    ticks = calcTicks()
    services = fetchServices()
        
    availableSlots = {}
    for serviceId, serviceTitle in services.items():
        if serviceIDS and serviceId not in serviceIDS:
            continue
        if DEBUG: print(f" - Fetching service: '{serviceTitle}' with ID: '{serviceId}'")
        slots = fetchSlotsByService(serviceId, ticks)
        if slots:
            availableSlots[serviceId] = {
                'slots':slots,
                'name':serviceTitle
            }
    
    if DEBUG: print(f" - Checked slots from '{checkedStartDate}'")
    
    return availableSlots

def main():
    serviceIDS = [
        106768, # Stallag privathäst morgon och lunch
        106769, # Stallag Privathäst insläpp och kväll
        106770, # Kvällsfodring privathäst
    ]
    s = fetchSlots(serviceIDS)
    print(s)

if __name__ == '__main__':
    main()
    