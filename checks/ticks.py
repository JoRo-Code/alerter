
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from time import sleep
import json

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

def getTodaysTicks() -> int:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    url = 'https://www.bokadirekt.se/boka-tjanst/heda-ridklubb-12384/stallag-foderv%C3%A4rd-morgon-och-eftermiddag-106767'
    driver.get(url)
    storage = SessionStorage(driver)
    sleep(1) # waiting for page to load
    try:
        bookDateStr = storage["bookDate"]
        d = json.loads(bookDateStr)
        ticks = d["timestamp"]
    except Exception as e:
        driver.close()
        raise Exception("Couldn't get todays timestamp. Adjust wait time", e)
    else:
        driver.close()
        return int(ticks)

if __name__ == '__main__':
    ticks = getTodaysTicks()
    print(ticks)


