class Message(object):
    def __init__(self, message_id, sender, date, body=''):
        self.message_id = message_id
        self.sender = sender
        self.date = date
        self.body = body

    def update_body(self, body):
        self.body = body

    def display(self):
        print_format = 'From: {}\nDate:{}\n\n{}'.format(self.sender, self.date, self.body)
        print(print_format)
