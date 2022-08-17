import os.path

from credentials import PASSWORD, EMAIL
from config import HOST, PORT, RECEIVERS

from alert.alerter import Alerter
from alert.sender import Sender
from alert.message import Message
from alert.check import Check
from alert.persistance import load_object

from checks.slots import fetchSlots
from checks.services import checkIsUpdatedServices

DEBUG = True

ENABLE_PERSISTANCE = True
script_dir = os.path.dirname(os.path.realpath(__file__))
CHECKS_FILE = script_dir + "/checks/" + "checks.pickle"

def main():
    sender = Sender(
        password= PASSWORD,
        email= EMAIL,
        host= HOST,
        port=PORT,
        debug=DEBUG,
    )
    
    receivers = RECEIVERS 
    
    foundSlotsMessage = Message(
        subject="Alert",
        body="Found slots",
    )
    
    foundServicesMessage = Message(
        subject="Alert",
        body="Found services",
    )
    
    # default checks
    checks = [
        Check(name="Slots",
              message = foundSlotsMessage,
              _check = fetchSlots,
              ),
        Check(name="Services",
              message = foundServicesMessage,
              _check = checkIsUpdatedServices,
              )
    ]

    # saved checks
    if ENABLE_PERSISTANCE:
        if os.path.exists(CHECKS_FILE):
            checks = load_object(CHECKS_FILE)
            if DEBUG: print("Loaded check info: " + str(checks[0]))
    
    
    a = Alerter(sender=sender,
                receivers = receivers,
                error_receivers = receivers,
                checks = checks,
                debug=DEBUG,
                )
    
    #a.run_with_waiting_time(wait_time=5, _break_func=a.isAllChecksAlerted)
    a.run(enablePersistance=ENABLE_PERSISTANCE, persistanceFile=CHECKS_FILE,)
    


if __name__ == '__main__':
    main()
    