
from message import Message
from time import sleep
from datetime import datetime

NEGATIVE_DETECTOR_MSG = "Negative detector: checked but false"
ERROR_SUBJECT_STR = "Error Message"
INIT_ALERTER_MSG = "Initalized Alerter"
CHECKING_DETECTOR_MSG = "Checking detector"
ALERT_MSG = "Detector True: Alerting all"

class Alerter():
    def __init__(self, 
                 sender, 
                 message, 
                 receivers, 
                 error_receivers, 
                 _detector, 
                 debug=False,
                 ):
        self.sender = sender
        self.message = message
        self.receivers = receivers
        self.error_receivers = error_receivers
        self._detector = _detector
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
    
    def run_with_waiting_time(self, wait_time, _break_func):
        self.scheduler(wait_time=wait_time, _callback=self.run,_detectorFunc=_break_func)

    def scheduler(self, wait_time, _callback, _detectorFunc):
        while not _detectorFunc():
            if self.debug: print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            sleep(wait_time)
            _callback()
         
    def run(self):
        try:
            if self.debug: print(CHECKING_DETECTOR_MSG)
            shouldAlert = self._detector()
            
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
                if self.debug: print(NEGATIVE_DETECTOR_MSG)
                
        
    
    