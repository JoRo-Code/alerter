from datetime import datetime

class Check():
    def __init__(self,
                 name, 
                 message,
                 _check, 
                 ):
        """
        :param func _check: function returning true if the check is positive (something happened)
        """
        self.name = name
        self.message = message
        self._check = _check
        self.isAlerted = False
        self.lastChecked = None
    
    def __str__(self):
        return f"Check(name: {self.name}, isAlerted: {self.isAlerted}, lastChecked: {self.lastChecked})"
        
    def run(self):
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        result = self._check()
        self.lastChecked = time
        return result
        
    def setAlerted(self):
        self.isAlerted = True
    
