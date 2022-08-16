
from message import Message
from time import sleep
from datetime import datetime

NEGATIVE_CHECK_MSG = "Negative check"
ERROR_SUBJECT_STR = "Error Message"
INIT_ALERTER_MSG = "Initalized Alerter"
CHECKING_CHECK_MSG = "Checking: "
ALERT_MSG = "Positive check: Alerting all"

class Alerter():
    def __init__(self, 
                 sender, 
                 receivers, 
                 error_receivers, 
                 checks,
                 debug=False,
                 ):
        self.sender = sender
        self.receivers = receivers
        self.error_receivers = error_receivers
        self.checks = checks
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
            
    def checkAlertAll(self, message):
        self.alertAll(self.receivers, message) 
        
    def errorAlertAll(self, error_message):
        self.alertAll(self.error_receivers, error_message) 
    
    def run_with_waiting_time(self, wait_time, _break_func):
        self.scheduler(wait_time=wait_time, _callback=self.run,_checkFunc=_break_func)

    def scheduler(self, wait_time, _callback, _checkFunc):
        while not _checkFunc():
            if self.debug: print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            sleep(wait_time)
            _callback()
         
    def run_check(self, check):
        try:
            if self.debug: print(CHECKING_CHECK_MSG + check.name)
            shouldAlert = check.run()
            
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
                self.checkAlertAll(check.message)
            else:
                if self.debug: print(NEGATIVE_CHECK_MSG)
    
    def run(self):
        for check in self.checks:
            self.run_check(check)
        
                
        
    
    