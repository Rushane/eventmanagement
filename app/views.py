"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from runapp import app, db
from flask import render_template, request, redirect, url_for, flash
from forms import LoginForm, RegistrationForm, EventForm
from models import *
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, make_response
import uuid
import jwt
import datetime
from functools import wraps
###
## Routing for your application.
###

# authenticated user by give them a token
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        print(request.headers)
        if 'X-Access-Token' in request.headers:
            token=request.headers['X-Access-Token']
        if not token:
            return jsonify({'message':'Token is not present!'})
        try:
            data =jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            current_user=EventManager.query.filter_by(manager_publicId=data['manager_publicId']).first()
            print(current_user)
        except Exception as e:
            print(e)
            return jsonify({'message':'Not a valid token!'}),401
        return f(current_user,*args,**kwargs)
    return decorated

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Authentication not verified",401,{"WWW-Authenticate":'Basic realm="Login Requried!"'})
    user = EventManager.query.filter_by(username=auth.username).first()
    if not user:
        return make_response("Authentication not verified",401,{"WWW-Authenticate":'Basic realm="Login Requried!"'})
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'manager_publicId':user.manager_publicId,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config["SECRET_KEY"])
        return jsonify({'token':token.decode('UTF-8')})
    return make_response("Authentication not verified",401,{"WWW-Authenticate":'Basic realm="Login Requried!"'})

@app.route("/api/users/register", methods=["POST"])
def register():
    form=RegistrationForm()
    if request.method == 'POST' :#and form.validate_on_submit():
        data = request.get_json()
        pword_hashed = data['password'] #generate_password_hash(data['password'],method='sha256')
        new_user = EventManager(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],telnum=data['telnum'] ,username=data['username'], password=pword_hashed, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'A new Event Manager user was created'})
    return render_template('register.html',form=form)

@app.route("/api/events/createEvent",  methods=["POST"])
@token_required
def createNewEvent(current_user):
    data =request.form
    files = request.files['flyer']
    photo=files
    filename= secure_filename(photo.filename)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_event = Event(name=data['name'], title=data['title'], category=data['category'], start_date=datetime.datetime.strptime(data['start_date'],"%Y/%m/%d"),
    end_date=datetime.datetime.strptime(data['end_date'],"%Y/%m/%d") ,description=data['description'], cost=data['cost'],venue=data['venue'], flyer=filename, managerid=data['managerid'],public=False)

    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event was created'})

# Should but not tested
@app.route('/api/events/<event_publicId>/public', methods=['PUT'])
@token_required
def makeEventPublic(current_user,event_publicId):
    record = Event.query.filter_by(event_publicId=event_publicId).first()
    if record is None:
        return jsonify({'message':'No events exist!'})
    else:
        record.public = True
        db.session.commit()
        return jsonify({'message':'Event was made public'})

@app.route('/api/events/<event_publicId>/viewEventInfo', methods=['GET'])
def viewEventInfo(event_publicId):
    event = Event.query.filter_by(event_publicId=event_publicId).first()
    if not event:
        return jsonify({'message':'This event does not exist!'})
    else:
        event_dict = dict()
        event_dict['eventid'] = event.eventid
        event_dict['name'] = event.name
        event_dict['title'] = event.title
        event_dict['category'] = event.category
        event_dict['start_date'] = event.start_date
        event_dict['end_date'] = event.end_date
        event_dict['description'] = event.description
        event_dict['venue'] = event.venue
        event_dict['flyer'] = event.flyer
        event_dict['managerid'] = event.managerid
        return jsonify({'message':event_dict})

@app.route("/api/events/<event_publicId>", methods=['PUT'])
#@token_required
def updateEventInfo(event_publicId):
    record = Event.query.filter_by(event_publicId=event_publicId).first()
    if record is None:
        return jsonify({'message':'No events exist!'})
    else:
        data =request.form
        files = request.files['flyer']
        photo=files
        filename= secure_filename(photo.filename)
        # get data FROM THE FORM
        name =  data['name']
        title = data['title']
        category = data['category']
        start_date = datetime.datetime.strptime(data['start_date'],"%Y/%m/%d")
        end_date = datetime.datetime.strptime(data['end_date'],"%Y/%m/%d")
        description = data['description']
        cost=data['cost']
        venue = data['venue']
        flyer = filename
        managerid = data['managerid']
        # ADD data to database
        record.name = name
        record.title = title
        record.category = category
        record.start_date = start_date
        record.end_date = end_date
        record.description = description
        record.cost=cost
        record.venue = venue
        record.flyer = flyer
        record.managerid = managerid
        db.session.commit()
        return jsonify({'message':'Event data was changed'})

@app.route('/api/events/<event_publicId>', methods=['DELETE'])
#@token_required
def deleteEvent(event_publicId):
    """ deletes event """
    eventrecord =  Event.query.filter_by(event_publicId=event_publicId).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    else:
        db.session.delete(eventrecord)
        db.session.commit()
        return jsonify({'message':'Event was deleted'})

# endpoint to get user detail by id
@app.route("/api/events/search/<eventname>", methods=["GET"])
def searchForEvent(eventname):
    events = Event.query.filter_by(name=eventname).all()
    event_list = []

    if events == []:
        return jsonify({'message':'This event does not exist!'})
    else:
        for event in events:
            event_dict = dict()
            event_dict['eventid'] = event.eventid
            event_dict['event_publicId'] = event.event_publicId
            event_dict['name'] = event.name
            event_dict['title'] = event.title
            event_dict['category'] = event.category
            event_dict['start_date'] = event.start_date
            event_dict['end_date'] = event.end_date
            event_dict['description'] = event.description
            event_dict['venue'] = event.venue
            event_dict['flyer'] = event.flyer
            event_dict['managerid'] = event.managerid
            event_list.append(event_dict)
        return jsonify({'events': event_list})

@app.route("/api/events/getAllEvents", methods=["GET"])
def getAllEvents():
    events = Event.query.all()
    event_list = []
    if events is None:
        return jsonify({'message':'No events exist!'})
    for event in events:
        event_dict = dict()
        event_dict['eventid'] = event.eventid
        event_dict['event_publicId'] = event.event_publicId
        event_dict['name'] = event.name
        event_dict['title'] = event.title
        event_dict['category'] = event.category
        event_dict['start_date'] = event.start_date
        event_dict['end_date'] = event.end_date
        event_dict['description'] = event.description
        event_dict['venue'] = event.venue
        event_dict['flyer'] = event.flyer
        event_dict['managerid'] = event.managerid
        event_list.append(event_dict)
    return jsonify({'events': event_list})

@app.route("/api/events/<event_publicId>/comment",methods=["POST"])
def commentOnEvent( event_publicId):
    """ comment on  events"""
    data = request.get_json()
    eventrecord =  Event.query.filter_by( event_publicId= event_publicId).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    else:
        comment= Comment(eventid=eventrecord.eventid,guestid=data['guestid'],comment=data['comment'])
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'comment was added to Event'})

@app.route("/api/events/<event_publicId>/rate",methods=["POST","Pevent_publicIdUT"])
def rateEvent(event_publicId):
    """ rating an events"""
    data = request.get_json()
    eventrecord =  Event.query.filter_by(event_publicId=event_publicId).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    else:
        raterecord = Rating.query.filter_by(eventid=eventrecord.eventid).first()
        if raterecord != None:
            oldrate=raterecord.rate_value
            raterecord.rate_value=(oldrate+data['rate_value'])/2
        else:
            rate= Rating(eventrecord.eventid, rate_value= data['rate_value'])
            db.session.add(rate)
        db.session.commit()
        return jsonify({'message': 'rating was added to Event'})






# which we can later use
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
