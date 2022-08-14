
from message import Message

NEGATIVE_CONDITION_MSG = "Negative condition: checked but false"
ERROR_SUBJECT_STR = "Error Message"
INIT_ALERTER_MSG = "Initalized Alerter"
CHECKING_CONDITION_MSG = "Checking condition"
ALERT_MSG = "Condition True: Alerting all"

class Alerter():
    def __init__(self, 
                 sender, 
                 message, 
                 receivers, 
                 error_receivers, 
                 _condition, 
                 debug=False
                 ):
        self.sender = sender
        self.message = message
        self.receivers = receivers
        self.error_receivers = error_receivers
        self._condition = _condition
        self.debug = debug
        
        if self.debug: print(INIT_ALERTER_MSG)
    
    def alert(self, receiver, message):
        m = message 
        self.sender.send_message(body=m.body,
                                subject=m.subject, 
                                receiver_address=receiver,
                                )

    def alertAll(self, receivers, message):
        for receiver in receivers:
            self.alert(receiver, message)
            
    def defaultAlertAll(self):
        self.alertAll(self.receivers, self.message)
        
    def errorAlertAll(self, error_message):
        self.alertAll(self.error_receivers, error_message) 
        
    def run(self):
        try:
            if self.debug: print(CHECKING_CONDITION_MSG)
            shouldAlert = self._condition()
            
        except Exception as e:
            if self.debug: print(e)
            
            message = Message(
                subject=ERROR_SUBJECT_STR,
                body=str(e),
                )
            
            self.errorAlertAll(error_message=message)
            
        else:
            if shouldAlert:
                if self.debug: print(ALERT_MSG)
                self.defaultAlertAll()
            else:
                if self.debug: print(NEGATIVE_CONDITION_MSG)
                
        
    
    