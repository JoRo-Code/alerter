
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from send.strings import MAIL_SENT_MSG, INIT_SENDER_MSG

class Sender():
    def __init__(self, 
                 password,
                 email,
                 host,
                 port,
                 debug=False,
                 ):
        self.password = password
        self.email = email
        self.host = host
        self.port = port
        self.debug = debug
        
        if self.debug: print(INIT_SENDER_MSG)
    
    def send_message(self, body, subject, receiver_address):
        sender_address = self.email
        sender_pass = self.password

        #Setup the MIME
        message = MIMEMultipart('alternative')
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject
        
        body = MIMEText(body, "html")
        message.attach(body)
        
        #Create SMTP session for sending the mail
        session = smtplib.SMTP(self.host, self.port) #use mail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password

        #sending message
        session.sendmail(sender_address, receiver_address, message.as_string())
        if self.debug: print(f"{MAIL_SENT_MSG} '{receiver_address}'")

        session.quit()
        
        