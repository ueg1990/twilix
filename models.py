from app import db

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
