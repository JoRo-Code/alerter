from send.sender import Sender
from alerter import Alerter
from credentials import PASSWORD, EMAIL
from config import HOST, PORT

DEBUG = True

class Message():
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        
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
    
    receivers= ["test@gmail.com"]
    
    a = Alerter(sender=sender, 
                message=message,
                receivers = receivers
                )
    
    a.alertAll()

if __name__ == '__main__':
    main()
    