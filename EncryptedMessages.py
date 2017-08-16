from Message import Message
from apiclient import discovery
import httplib2

class EncryptedMessages(object):
    def __init__(self, credentials):
        self.credentials = credentials
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=self.http)

    def list_messages(self):
        messages_list = self.get_encrypted_message_list()
        for message in messages_list:
            format = 'Recieved: {}\n\tFrom: {}'.format(message.date, message.sender)
            print(format)

    def get_encrypted_message_ids(self):
        query = 'subject:[encEmail]'
        results = self.service.users().messages().list(userId='me', labelIds=None, q=query).execute()
        messages = results.get('messages', [])
        message_ids = [message['id'] for message in messages]
        return message_ids

    def get_encrypted_message_list(self):
        message_ids = self.get_encrypted_message_ids()
        messages_json_list, messages_list = [], []
        for message_id in message_ids:
            metadata_headers = ['From', 'Date']
            params = {'userId': 'me',
                      'id': message_id,
                      'format': 'metadata',
                      'metadataHeaders': metadata_headers
                      }
            messages_json_list += [self.service.users().messages().get(**params).execute()]
        for message in messages_json_list:
            sender = [entry['value'] for entry in message['payload']['headers'] if entry['name'] == 'From'][0]
            date = [entry['value'] for entry in message['payload']['headers'] if entry['name'] == 'Date'][0]
            messages_list += [Message(sender, date)]
        return messages_list