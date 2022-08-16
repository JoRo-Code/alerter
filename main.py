from send.sender import Sender
from alerter import Alerter
from credentials import PASSWORD, EMAIL
from config import HOST, PORT
from detector.slots import fetchSlots
from detector.services import checkIsUpdatedServices
from message import Message
from check import Check

DEBUG = True

        
def main():
    sender = Sender(
        password= PASSWORD,
        email= EMAIL,
        host= HOST,
        port=PORT,
        debug=DEBUG,
    )
    
    receivers= ["test@gmail.com",
                ]
    
    foundSlotsMessage = Message(
        subject="Alert",
        body="Found slots",
    )
    
    foundServicesMessage = Message(
        subject="Alert",
        body="Found services",
    )
    
    
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
    
    
    a = Alerter(sender=sender,
                receivers = receivers,
                error_receivers = receivers,
                checks = checks,
                debug=DEBUG,
                )
    
    a.run_with_waiting_time(wait_time=5, _break_func=lambda: False)

if __name__ == '__main__':
    main()
    