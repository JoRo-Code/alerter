import os.path
from credentials import PASSWORD, EMAIL
from config import HOST, PORT, RECEIVERS

from alert.alerter import Alerter
from alert.sender import Sender
from alert.message import Message
from alert.check import Check

from checks.slots import fetchSlots
from checks.services import checkIsUpdatedServices

DEBUG = True

script_dir = os.path.dirname(os.path.realpath(__file__))
CHECKS_FILE = script_dir + "/checks/" + "checks.pickle"
LOG_FILE= script_dir + "/" + "logger.json"

serviceIDS = [
    106768, # Stallag privathäst morgon och lunch
    106769, # Stallag Privathäst insläpp och kväll
    #106770, # Kvällsfodring privathäst
]

def fetchSlotIDS():
    return fetchSlots(serviceIDS)

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
    
    changedServicessMessage = Message(
        subject="Alert",
        body="Services info changed",
    )


    
    # default checks
    checks = [
        Check(name="Available slots",
              message = foundSlotsMessage,
              _check = fetchSlotIDS,
              ),
        Check(name="Changed services info",
              message = changedServicessMessage,
              _check = checkIsUpdatedServices,
              ),
    ]

    a = Alerter(sender=sender,
                receivers = receivers,
                error_receivers = [receivers[0]], # first receiver
                checks = checks,
                debug=DEBUG,
                persistanceFile=CHECKS_FILE,
                loggerFile=LOG_FILE,
                )
    
    #a.run_with_waiting_time(wait_time=5, _break_func=a.isAllChecksAlerted)
    a.run()
    


if __name__ == '__main__':
    main()
    