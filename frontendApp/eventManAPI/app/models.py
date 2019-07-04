from runapp import db
import uuid
from werkzeug.security import generate_password_hash

class Guest(db.Model):

    __tablename__ = 'Guest'

    guestid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180))
    displayName = db.Column(db.String(80), unique=True)

    def __init__(self, email, displayName):
        self.displayName = displayName
        self.email = email

    def is_authenticated(self):
        return False

    def is_admin(self):
        return False

    def is_guest(self):
        return True

    def get_userId(self):
        try:
            return unicode(self.guestid)  # python 2 support
        except NameError:
            return str(self.guestid)  # python 3 support


class EventManager(db.Model):

    __tablename__ = 'EventManager'

    managerid = db.Column(db.Integer, primary_key=True)
    manager_publicId = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    telnum = db.Column(db.String(180))
    email = db.Column(db.String(180))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)

    def __init__(self, first_name, last_name, email, telnum, username, password, admin):
        self.manager_publicId = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.telnum = telnum
        self.email = email
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
        self.admin = admin

    def is_authenticated(self):
        return True if not self.admin else False

    def is_admin(self):
        return True if self.admin else False

    def is_guest(self):
        return False

    def __repr__(self):
        return '<User: %r>' % (self.username)

    def get_userId(self):
        try:
            return unicode(self.managerid)  # python 2 support
        except NameError:
            return str(self.managerid)  # python 3 support

    def get_publicId(self):
        try:
            return unicode(self.manager_publicId)  # python 2 support
        except NameError:
            return str(self.manager_publicId)  # python 3 support


class Event(db.Model):

    __tablename__ = 'Event'

    eventid = db.Column(db.Integer,primary_key=True)
    event_publicId = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    title = db.Column(db.String(50), nullable= False)
    category = db.Column(db.String(50))
    start_date = db.Column(db.DateTime, nullable= False)
    end_date = db.Column(db.DateTime, nullable= False)
    description= db.Column(db.String(1000), nullable= False)
    cost = db.Column(db.Float(10))
    venue = db.Column(db.String(50))
    flyer = db.Column(db.Text)
    public = db.Column(db.Boolean)
    managerid = db.Column(db.Integer, db.ForeignKey ('EventManager.managerid'))

    def __init__(self, name, title, category, start_date, end_date, description, cost, venue, flyer, managerid, public):
        self.event_publicId = str(uuid.uuid4())
        self.name = name
        self.title = title
        self.category = category
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.cost = cost
        self.venue = venue
        self.flyer = flyer
        self.managerid = managerid
        self.public = public

    def get_eventId(self):
        try:
            return unicode(self.eventid)  # python 2 support
        except NameError:
            return str(self.eventid)  # python 3 support

    def get_eventPublicId(self):
        try:
            return unicode(self.event_publicId)  # python 2 support
        except NameError:
            return str(self.event_publicId)  # python 3 support


class Comment(db.Model):

    __tablename__ = 'Comment'

    commentid = db.Column(db.Integer,primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey ('Event.eventid'))
    guestid = db.Column(db.Integer, db.ForeignKey ('Guest.guestid'))
    comment = db.Column(db.String(50))

    def __init__(self, eventid, guestid, comment):
        self.eventid = eventid
        self.guestid = guestid
        self.comment = comment

    def get_commentId(self):
        try:
            return unicode(self.commentid)  # python 2 support
        except NameError:
            return str(self.commentid)  # python 3 support




class Rating(db.Model):

    __tablename__ = 'Rating'

    rateid = db.Column(db.Integer,primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey ('Event.eventid'))
    rate_value = db.Column(db.Integer)

    def __init__(self, eventid, rate_value):
        self.eventid = eventid
        self.rate_value = rate_value

    def get_ratingId(self):
        try:
            return unicode(self.rateid)  # python 2 support
        except NameError:
            return str(self.rateid)  # python 3 support
