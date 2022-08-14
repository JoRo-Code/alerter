from send.sender import Sender
from alerter import Alerter
from credentials import PASSWORD, EMAIL
from config import HOST, PORT
from condition.condition import fetchSlots
from message import Message

DEBUG = True

        
def main():
    sender = Sender(
        password= PASSWORD,
        email= EMAIL,
        host= HOST,
        port=PORT,
        debug=DEBUG,
    )
    
    message = Message(
        subject="Test subject",
        body="Test body",
    )
    
    receivers= ["test@gmail.com",
                ]
    
    a = Alerter(sender=sender, 
                message=message,
                receivers = receivers,
                error_receivers = receivers,
                _condition = fetchSlots,
                debug=DEBUG,
                )
    
    a.run()

if __name__ == '__main__':
    main()
    