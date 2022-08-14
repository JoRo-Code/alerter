
class Alerter():
    def __init__(self, sender, message, receivers):
        self.sender = sender
        self.message = message
        self.receivers = receivers

    def alertAll(self):
        for receiver in self.receivers:
            self.alert(receiver)
            
    def alert(self, receiver):
        m = self.message 
        self.sender.send_message(body=m.body,
                    subject=m.subject, 
                    receiver_address=receiver,
                    )
    def run(self):
        pass
        
    
    