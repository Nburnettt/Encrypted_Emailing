from __future__ import print_function
import os
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


def display_menu():
    menu = 'Commands:\n'
    menu += '\texit - Leave the terminal\n'
    menu += '\tinbox - Display user inbox\n'
    menu += '\tview <num> - View message num (listed by inbox)\n'
    menu += '\thelp - Displays this menu\n'
    print(menu)


def get_user_input():
    menu = ': '
    user_input = input(menu)
    return user_input


def error():
    print('Invalid Command')
    display_menu()


def main():
    credentials = get_credentials()
    encrypted_messages = EncryptedMessages(credentials)
    user_input = [1]
    display_menu()
    while user_input[0] != 'exit':
        user_input = get_user_input().split(' ')
        num_args = len(user_input)
        if num_args == 1:
            if user_input[0] == 'inbox':
                encrypted_messages.list_messages()
            elif user_input[0] == 'help':
                display_menu()
            else:
                error()
        elif num_args == 2:
            if user_input[0] == 'view':
                message_index = int(user_input[1])
                encrypted_messages.display_message(message_index)
            else:
                error()


if __name__ == '__main__':
    main()
