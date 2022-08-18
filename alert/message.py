import json

class Message():
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
    
    def __str__(self):
        return f"Message(subject: {self.subject}, body: {self.body})"
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
            