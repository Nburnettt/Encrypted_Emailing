class Message(object):
    def __init__(self, sender, date, body=''):
        self.sender = sender
        self.date = date
        self.body = body