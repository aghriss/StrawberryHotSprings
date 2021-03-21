# !pip install twilio
from twilio.rest import Client
import config

class Notifier():
    """
        Class to send SMS and check for inbound SMS
    """
    
    def __init__(self):
        
        self.client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
    def notify(self, message):
        try:
            message = self.client.messages.create(
                    body =  message, #Message you send
                    from_ = config.TWILIO_NUMBER, # Account N
                    to =    config.TARGET_NUMBER)#Your phone number
        except:
            print("Couldn't send SMS, service has been probably stopped")
        return message
        
            
    def last_received(self):
        response = self.client.messages.list(from_=config.TARGET_NUMBER, limit=1)
        if response:
            return response[0]
        return None