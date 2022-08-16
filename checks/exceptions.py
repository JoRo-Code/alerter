class CheckException(Exception):
    def __init__(self, message, name="FetchError"):
        self.message = message
        self.name = name
        
        super().__init__(self.message)
    
    def __str__(self):
        return self.name + ": " + self.message

class ParseException(CheckException):
    """Raised when the data couldn't be parsed"""
    def __init__(self, message):
        self.message = message
        self.name = "ParseException"
        
        
class FetchException(CheckException):
    """Raised when the data couldn't be fetched"""
    def __init__(self, message):
        self.message = message
        self.name = "FetchException"
        
        super().__init__(self.message, self.name)
    