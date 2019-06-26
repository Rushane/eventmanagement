"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import EventManager, Event
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
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is not present!'})
        try:
            data =jwt.decode(token,app.config['SECRET_KEY'])
            current_user=EventManager.query.filter_by(manager_publicId=data['manager_publicId']).first()
        except Exception as e:
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


@app.route("/login", methods=["GET", "POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Authentication not verified",401,{"WWW-Authenticate":'Basic realm="Login Requried!"'})
    user = EventManager.query.filter_by(name=auth.username).first()
    if not user:
        return make_response("Authentication not verified",401,{"WWW-Authenticate":'Basic realm="Login Requried!"'})
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config["SECRET_KEY"])
        return jsonify({'token':token.decode('UTF-8')})
    return make_response("Authentication not verified",401,{"WWW-Authenticate":'Basic realm="Login Requried!"'})
    pass

@app.route("/api/users/register",  methods=["POST"])
def register():
    data = request.get_json()
    pword_hashed = generate_password_hash(data['password'],method='sha256')
    new_user = EventManager(public_id=data['public_id']first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
    telnum=data['telnum'] ,username=data['username'], password=pword_hashed, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'The Event Manager user was created'})

# how to post image in postman: https://stackoverflow.com/questions/39660074/post-image-data-using-postman
@app.route("/api/events/createEvent",  methods=["POST"])
#@token_required
def createNewEvent():
    #date_created = datetime.datetime.now().strftime("%B %d, %Y")
    data = request.get_json()
    print(data)
    imagefile = request.files.get('imagefile', '')
    print(imagefile)
    #imagefile.save('C:/Users/Real/Desktop/ems-starter/app/static/images')
    #filename = secure_filename(imagefile.filename)
    #imagefile.save(os.path.join("./app",app.config['UPLOAD_FOLDER'], filename))
    #imagefile.save('C:\Users\Real\Desktop\ems-starter\app\static\' + imagefile)

    new_event = Event(name=data['name'], title=data['title'], category=data['category'], start_date=data['start_date'] ,
    end_date=data['end_date'] ,description=data['description'], cost=data['cost'],venue=data['venue'], flyer=imagefile)
    # The picture thingy with Flyer not working
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event was created'})

# Should but not tested
@app.route('/api/events/<eventID>/public', methods=['PUT'])
#@token_required
def makeEventPublic(eventid):
    record = Event.query.filter_by(eventid=eventid).first()
    
    record.public = True
    db.session.commit()

    return jsonify({'message':'Event was made public'})

@app.route('/api/events/<eventid>/viewEventInfo', methods=['GET'])
def viewEventInfo(eventid):
    event = Event.query.filter_by(eventid=eventid).first()
    if not event:
        return jsonify({'message':'This event does not exist!'})
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

    return jsonify({'message':'Event shown!'})

@app.route("/api/events/<eventid>", methods=['PUT'])
def updateEventInfo(eventid): 
    record = Event.query.filter_by(eventid=eventid).first()
    #form = EventForm(request.form, obj=record)
    name =  request.json['name'] 
    title = request.json['title']
    category = request.json['category']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    description = request.json['description']
    venue = request.json['venue']
    flyer = request.json['flyer']

    record.name = name
    record.title = title
    record.category = category
    record.start_date = start_date
    record.end_date = end_date
    record.description = description
    record.venue = venue
    record.flyer = flyer

    db.session.commit()
    return jsonify({'message':'Event data was changed'})
    
@app.route('/api/events/<eventid>/delete', methods=['DELETE'])
#@token_required
def deleteEvent(eventid):
    """ deletes event """
    eventrecord =  Event.query.filter_by(eventid=eventid).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    db.session.delete(eventrecord)
    db.session.commit()

    return jsonify({'message':'Event was deleted'})

# endpoint to get user detail by id
@app.route("/api/events/search", methods=["GET"])
def searchForEvent(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route("/api/events/<eventid>/comment",methods="POST")
def commentOnEvent(eventid):
    """ comment on  events"""
    data = request.get_json()
    eventrecord =  Event.query.filter_by(eventid=eventid).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    else:
        comment= Comment(comment_publicId=str(uuid.uuid4()),eventid=eventid,guestid=data['guestid'],comment=data['comment'])
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'comment was added to Event'})

@app.route("/api/events/<eventid>/rate",methods="POST")
def rateEvent(eventid):
    """ rating an events"""
    eventrecord =  Event.query.filter_by(eventid=eventid).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    else:
        raterecord = Rating.query.filter_by(eventid=eventid).first()
        rate=""
        if raterecord != None:
            oldrate=raterecord.rate_value
            rate= Rating(rating_publicId=data["rating_publicId"], eventid=eventid, rate_value= (old+data['rate_value'])/2)
        else:
            rate= Rating(rating_publicId=data["rating_publicId"], eventid=eventid, rate_value= data['rate_value'])
        db.session.add(rate)
        db.session.commit()
        return jsonify({'message': 'rating was added to Event'})





# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
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


if __name__ == '__main__':
    app.run(debug=True)
