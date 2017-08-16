from Message import Message
from apiclient import discovery
import httplib2
import base64


class EncryptedMessages(object):
    def __init__(self, credentials):
        self.credentials = credentials
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=self.http)
        self.messages = []

    def list_messages(self):
        self.update_messages()
        for i, message in enumerate(self.messages):
            print_format = '#{}\n\tRecieved: {}\n\tFrom: {}'.format(i, message.date, message.sender)
            print(print_format)

    def display_message(self, message_index):
        message = self.messages[message_index]
        params = {'userId': 'me',
                  'id': message.message_id,
                  'format': None,
                  'metadataHeaders': None
                  }
        message_json = self.service.users().messages().get(**params).execute()
        encoded_body = message_json['payload']['parts'][0]['body']['data']
        body = base64.standard_b64decode(encoded_body).decode('utf-8')
        message.update_body(body)
        message.display()

    def get_encrypted_message_ids(self):
        query = 'subject:[encEmail]'
        results = self.service.users().messages().list(userId='me', labelIds=None, q=query).execute()
        messages = results.get('messages', [])
        message_ids = [message['id'] for message in messages]
        return message_ids

    def update_messages(self):
        message_ids = self.get_encrypted_message_ids()
        messages_json_list, messages_list = [], []
        for message_id in message_ids:
            metadata_headers = ['From', 'Date']
            params = {'userId': 'me',
                      'id': message_id,
                      'format': 'metadata',
                      'metadataHeaders': metadata_headers
                      }
            messages_json_list += [(message_id, self.service.users().messages().get(**params).execute())]
        for message_id, message in messages_json_list:
            sender = [entry['value'] for entry in message['payload']['headers'] if entry['name'] == 'From'][0]
            date = [entry['value'] for entry in message['payload']['headers'] if entry['name'] == 'Date'][0]
            messages_list += [Message(message_id, sender, date)]
        self.messages = messages_list
