
import pickle

from tinydb import TinyDB
from datetime import datetime

def save_object(obj, filename):
    try:
        with open(filename, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex) 

def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)
    

class Logger():
    def __init__(self, loggerFile):
        self.db = TinyDB(loggerFile)
    
    def add(self, item):
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log = {
            'time': time,
            'item': item,
        }
        self.db.insert(log)
    
    def show(self):
        for item in self.db.all():
            print(item)
        