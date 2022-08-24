import os.path

from alert.message import Message
from time import sleep
from datetime import datetime

from alert.persistance import save_object, load_object
from alert.persistance import Logger

NEGATIVE_CHECK_MSG = "Negative check"
ERROR_SUBJECT_STR = "Error Message"
INIT_ALERTER_MSG = "Initialized Alerter"
CHECKING_CHECK_MSG = "Checking: "
ALREADY_ALERTED_MSG= "Skipping already alerted check: "
ALERT_MSG = "Positive check: Alerting all"

class Alerter():
    def __init__(self, 
                 sender, 
                 receivers, 
                 error_receivers, 
                 checks,
                 debug=False,
                 persistanceFile=None,
                 loggerFile=None,
                 ):
        self.sender = sender
        self.debug = debug
        self.receivers = receivers
        self.error_receivers = error_receivers
        self.persistanceFile = persistanceFile
        
        if os.path.exists(persistanceFile):
            checks = load_object(persistanceFile)
            if self.debug: 
                print(f"Loaded checks: ")
                for check in checks:
                    print(" - " + str(check))
        
        self.checks = checks
        
        self.logger = None
        if loggerFile:
            self.logger = Logger(loggerFile=loggerFile)
        
        if self.debug: print(INIT_ALERTER_MSG)
    
    def log(self, message):
        if self.logger:
            log = {'message':str(message),
                'checks': [str(x) for x in self.checks],
            }
            self.logger.add(log)
        
    def alert(self, receiver, message):
        m = message 
        self.sender.send_message(body=m.body,
                                subject=m.subject, 
                                receiver_address=receiver,
                                )
        self.log(message=message)

    def alertAll(self, receivers, message):
        for receiver in receivers:
            self.alert(receiver, message)
            
    def checkAlertAll(self, check):
        check.setAlerted()
        self.alertAll(self.receivers, check.message) 
        
    def errorAlertAll(self, error_message):
        self.alertAll(self.error_receivers, error_message) 
    
    def run_with_waiting_time(self, wait_time, _break_func):
        self.scheduler(wait_time=wait_time, _callback=self.run,_checkFunc=_break_func)

    def scheduler(self, wait_time, _callback, _checkFunc):
        while not _checkFunc():
            if self.debug: print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            sleep(wait_time)
            _callback()
    
    def isAllChecksAlerted(self):
        for check in self.checks:
            if not check.isAlerted:
                return False
        return True
            
         
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
                self.checkAlertAll(check)
            else:
                if self.debug: print(NEGATIVE_CHECK_MSG)
    
    def run(self):
            
        for check in self.checks:
            if check.isAlerted:
                if self.debug: print(ALREADY_ALERTED_MSG + check.name)
                continue
            self.run_check(check)
        
        if self.persistanceFile:
            save_object(self.checks, self.persistanceFile)
            
        
                
        
    
    