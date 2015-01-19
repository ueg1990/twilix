from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from twilio import twiml
import subprocess
import os

from cmd import cmds

app = Flask(__name__)
#app.config.from_object('config')
db = SQLAlchemy(app)

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
APP_SID = os.environ['APP_SID']
CALLER_ID = os.environ['CALLER_ID']

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
	    args[index] = arg.lower().split()
        output = cmds['pipe'](args)
    else:
	args = user_input.lower().split() 
        output = cmds[args[0]](args)
    response.sms(output)
    return str(response)

if __name__ == "__main__":
    #app.run(debug=True)
    app.debug = True
    app.run(host='0.0.0.0')
