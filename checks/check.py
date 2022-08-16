
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
        
    def run(self):
        return self._check()
        
    def setAlerted(self):
        self.isAlerted = True
