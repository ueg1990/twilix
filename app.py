from flask import Flask, redirect, url_for, render_template, request 
from flask.ext.sqlalchemy import SQLAlchemy
import os
import subprocess

from forms import UserRegistrationForm 

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY'] 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
#db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    server_url = db.Column(db.String(120), index=True)
    server_user = db.Column(db.String(60), index=True)
    server_password = db.Column(db.String(24))
    email = db.Column(db.String(120), index=True)
    twilio_number = db.Column(db.String(60), index=True)

    def __init__(self, email, server_url, server_user, server_password,twilio_number):
        self.email = email
        self.server_url = server_url
        self.server_user = server_user
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
	#user = User(form.email.data, form.server_url.data, form.server_user.data,form.server_password.data, form.twilio_number.data)
	#db.session.add(user)
	#db.session.commit()
        subprocess.call("fab -H {0} -u {1} -p {2} create".format(form.server_url.data, form.server_user.data,form.server_password.data), shell=True)
	return redirect(url_for('bye'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run(host='0.0.0.0')
