from . import db
from werkzeug.security import generate_password_hash

class EventManager(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'event_manager'

    userid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(180))
    telnum = db.Column(db.String(180))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)
    
    # def __init__(self, first_name, last_name, email, telnum, username, password):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.telnum = telnum
    #     self.username = username
    #     self.password = generate_password_hash(password, method='pbkdf2:sha256')
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)


class Event(db.Model):
	eventid = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))
	title = db.Column(db.String(50), nullable= False)
	category = db.Column(db.String(50))
	start_date = db.Column(db.DateTime, nullable= False)
	end_date = db.Column(db.DateTime, nullable= False)
	description= db.Column(db.String(1000), nullable= False) 
	cost = db.Column(db.Float(10))
	venue = db.Column(db.String(50))
	flyer = db.Column(db.Text)
	creator = db.Column(db.Integer,db.ForeignKey ('event_manager.userid'))

class Comment(db.Model):
	commentid = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(50))
	comment = db.Column(db.String(50))
	eventid = db.Column(db.Integer,db.ForeignKey ('event.eventid'))

class Rating(db.Model):
	rateid = db.Column(db.Integer,primary_key=True)
	rate_value = db.Column(db.String(50))
	eventid = db.Column(db.Integer,db.ForeignKey ('event.eventid'))

class Guest(db.Model):
	guestid = db.Column(db.Integer,primary_key=True)
	displayname= db.Column(db.String(50))
	email = db.Column(db.String(180))

# class Assigns(db.Model):
#     rateid = db.Column(db.Integer,db.ForeignKey ('rating.rateid'))
#     userid = db.Column(db.Integer,db.ForeignKey ('eventmanager.userid'))
#     userid = db.Column(db.Integer,db.ForeignKey ('eventmanager.userid'))
