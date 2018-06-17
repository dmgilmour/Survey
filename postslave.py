# the post slave

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import base64

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase


class PostSlave:

    # Default MACROS

    FROM_ADDRESS = 'engr.academics@gmail.com'
    service = ''

    def __init__(self):

        # Setup the Gmail API
        SCOPES = 'https://www.googleapis.com/auth/gmail.send'
        store = file.Storage('email_credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('email_apikey.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

    def create_message(self, to, subject, body, from_address = FROM_ADDRESS):
        message = MIMEText(body)
        message['to'] = to
        message['from'] = from_address
        message['subject'] = subject 
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def send_message(self, message, user_id = 'me'):
        message = (self.service.users().messages().send(userId=user_id, body=message)
                   .execute())
        return message
