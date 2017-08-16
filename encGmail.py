from __future__ import print_function
import httplib2
import os
import base64
from EncryptedMessages import EncryptedMessages

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    encrypted_messages = EncryptedMessages(credentials)
    message_ids = encrypted_messages.get_encrypted_message_ids()
    encrypted_messages.list_messages()
    #     results = service.users().messages().get(**params).execute()
    #     messages_list += [results]
    # for message in messages_list:
    #     message_from = [entry['value'] for entry in message['payload']['headers']
    #                     if entry['name'] == 'From'][0]
        # encoded_body = message['payload']['parts'][0]['body']['data']
        # body = base64.standard_b64decode(encoded_body).decode('utf-8')
        # print(message['payload']['headers'])
        # print(body)

if __name__ == '__main__':
    main()
