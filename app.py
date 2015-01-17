from flask import Flask, redirect, url_for, render_template, request 
from flask.ext.sqlalchemy import SQLAlchemy
import os

from forms import UserRegistrationForm 

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    server_url = db.Column(db.String(120), index=True, unique=True)
    server_password = db.Column(db.String(24))
    email = db.Column(db.String(120), index=True, unique=True)
    twilio_number = db.Column(db.String(60), index=True, unique=True)

    def __init__(self, email, server_url, server_password,twilio_number):
        self.email = email
        self.server_url = server_url
        self.server_password = server_password
        self.twilio_number = self._format_number(twilio_number)

    def _format_number(self, number):
        if number[:2] != '+1':
            return '+1' + number
        return number

    def __repr__(self):
        return '<User %r>' % (self.email)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye/")
def bye():
    return "Bye World!!!"

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
	return redirect(url_for('bye'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
