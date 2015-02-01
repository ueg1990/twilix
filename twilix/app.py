from flask import Flask, request
from twilio import twiml
import subprocess
import os

from cmd import cmds

app = Flask(__name__)

USER_NUMBER = os.environ["USER_NUMBER"]

@app.route("/")
def index():
    return "Hello, world!!!!"

@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    user_input = request.form['Body']
    user_from = request.form['From']
    if user_from != USER_NUMBER:
        output = "This number is not registered with this server"
    else:
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
    #app.debug = True
    #app.run(host='0.0.0.0')
    app.run()
