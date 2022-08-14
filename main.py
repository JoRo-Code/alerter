from blinker import receiver_connected
from alerter.alerter import Alerter
from credentials import PASSWORD, EMAIL
from config import HOST, PORT

DEBUG = True

def main():
    a = Alerter(
        password= PASSWORD,
        email= EMAIL,
        host= HOST,
        port=PORT,
        debug=DEBUG,
    )
    
    body = "Test body"
    subject = "Test subject"
    receiver_address = "test@gmail.com"
    
    a.send_message(body=body,
                   subject=subject, 
                   receiver_address=receiver_address,
                   )

if __name__ == '__main__':
    main()
    