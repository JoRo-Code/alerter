
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from time import sleep
import json
from typing import Tuple
from datetime import datetime

class SessionStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.sessionStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.sessionStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.sessionStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.sessionStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.sessionStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.sessionStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.sessionStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
    

import os
script_dir = os.path.dirname(os.path.realpath(__file__))
ticks_file = script_dir + "/" + "ticks.json"

def readTicksFromMemory() -> Tuple[int, datetime]:
    try:
        with open(ticks_file, "r") as f:
            ticks_info = json.load(f)
            
            ticks = ticks_info["ticks"]
            raw_date = ticks_info["timestamp"]
            date = datetime.strptime(raw_date, "%d/%m/%Y %H:%M:%S")
    except:
        with open(ticks_file, 'w') as f:
            f.write('')
        
        ticks = 0
        date = datetime(2000, 1,1)

    return ticks, date

def saveTicksInMemory(ticks:int):    
    
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ticks_info = {
        'ticks': ticks,
        'timestamp': time,
    }
    with open(ticks_file, 'w') as f:
        json.dump(ticks_info, f, ensure_ascii=False, indent=4)
    

def getTodaysTicks() -> int:
    def get_week(date:datetime) -> int:
        return date.isocalendar().week
    update_ticks_interval = 60*60*24 # once a day
    ticks, date = readTicksFromMemory()
    now = datetime.now()
    is_new_week = get_week(date) != get_week(now)
    if (now-date).total_seconds() > update_ticks_interval or is_new_week:
        ticks = getTodaysTicksFromBrowser()
        saveTicksInMemory(ticks)
    return ticks
         

def getTodaysTicksFromBrowser(sleep_time:int=1) -> int: 
    if sleep_time > 50:
        # infinite loop handler
        raise Exception("Sleep time is extremely high, terminating")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    url = 'https://www.bokadirekt.se/boka-tjanst/heda-ridklubb-12384/stallag-foderv%C3%A4rd-morgon-och-eftermiddag-106767'
    driver.get(url)
    storage = SessionStorage(driver)
    sleep(sleep_time) # waiting for page to load
    try:
        bookDateStr = storage["bookDate"]
        d = json.loads(bookDateStr)
        ticks = d["timestamp"]
    except:
        return getTodaysTicksFromBrowser(sleep_time=sleep_time*2)
    else:
        driver.close()
        return int(ticks)

if __name__ == '__main__':
    ticks = getTodaysTicks()
    print(ticks)


