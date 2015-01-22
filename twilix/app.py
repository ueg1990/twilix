from flask import Flask, request
from twilio import twiml
import subprocess
import os

from cmd import cmds

app = Flask(__name__)

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
APP_SID = os.environ['TWILIO_APP_SID']
CALLER_ID = os.environ['TWILIO_CALLER_ID']

@app.route("/")
def index():
    return "Hello, world"

@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    user_input = request.form['Body']
    if '|' in user_input:
        args = user_input.split('|')
        for index, arg in enumerate(args):
	    args[index] = arg.split()
        output = cmds['pipe'](args)
    else:
	args = user_input.split() 
        output = cmds[args[0]](args)
    response.sms(output)
    return str(response)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
