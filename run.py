from flask import Flask, request, render_template, Response
from twilio.jwt.client import ClientCapabilityToken
from twilio.twiml.voice_response import Dial, VoiceResponse, Say

import os
import re

app = Flask(__name__, static_folder='app/static')

# Add a Twilio phone number or number verified with Twilio as the caller ID
caller_id = os.environ.get("Twilio_caller_id")
default_client = "Jenny"

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    dest_number = request.values.get('PhoneNumber', None)
    default_client = request.values.get('PhoneNumber', None)
    resp = VoiceResponse()
    # item = request.values.get('item', None)
    # name = request.values.get('name', None)
 
    with resp.dial(callerId=caller_id, record='true') as r:

    # If we have a number, and it looks like a phone number:
        if dest_number and re.search('^[\d\(\)\- \+]+$', dest_number): 
            r.number(dest_number)
        else:
            r.client(default_client)
    return str(resp)
@app.route('/test', methods=['POST', 'GET'])
def dialer():

    return(render_template('index.html'))

@app.route('/incoming_call', methods=['POST'])
def call():
    resp = VoiceResponse()
    with resp.dial(callerId=caller_id, record='true') as r:
      r.client('TomPY')
    return str(resp)   
 
@app.route('/', methods=['GET', 'POST'])
def client():
    """Respond to incoming requests."""
    client_name = request.values.get('client', None) or "TomPY"
    
    account_sid = os.environ.get("Twilio_account_sid")
    auth_token = os.environ.get("Twilio_auth_token")
 
    # This is a special Quickstart application sid - or configure your own
    # at twilio.com/user/account/apps
    application_sid = os.environ.get("Twilio_application_sid")
    capability = ClientCapabilityToken(account_sid, auth_token)

    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming(client_name)
    
    
    token = capability.to_jwt()
    print(capability.to_jwt())
 
    return render_template('index.html', token=token.decode("utf-8"), client_name=client_name)
 
if __name__ == "__main__":
    app.run(debug=True)
