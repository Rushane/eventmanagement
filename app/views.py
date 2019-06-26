"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import EventManager, Event
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, make_response
import uuid
import jwt
import datetime
from functools import wraps
###
# Routing for your application.
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
            current_user=EventManager.query.filter_by(public_id=data['public_id']).first()
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
    new_user = EventManager(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
    telnum=data['telnum'] ,username=data['username'], password=pword_hashed, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'The Event Manager user was created'})

# how to post image in postman: https://stackoverflow.com/questions/39660074/post-image-data-using-postman
@app.route("/api/events/createEvent",  methods=["POST"])
def createNewEvent():
    #date_created = datetime.datetime.now().strftime("%B %d, %Y")
    data = request.get_json()
    new_event = Event(name=data['name'], title=data['title'], category=data['category'], start_date=data['start_date'] ,
    end_date=data['end_date'] ,description=data['description'], cost=data['cost'],venue=data['venue'], flyer=data['flyer'])
    # The picture thingy with Flyer not working
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event was created'})

# Should but not tested
@app.route('/api/events/<eventID>/public', methods=['PUT'])
def makeEventPublic(eventid):
    record = Event.query.filter_by(eventid=eventid).first()

    record.eventstatus = "Public"
    db.session.commit()

    return jsonify({'message':'Event was made public'})

@app.route('/api/events/<eventid>/viewEventInfo', methods=['GET'])
def viewEventInfo(eventid):
    """Render details of particular event."""
    result=Event.query.filter_by(eventid=eventid).first()

    return render_template('viewEvent.html', result=result)

@app.route("/api/events/<eventid>/update", methods=['GET', 'POST'])
def updateEventInfo(eventid):
    record = Event.query.filter_by(eventid=eventid).first()
    form = EventForm(request.form, obj=record)

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(record)

        db.session.commit()
        flash('Event {} Updated!'.format(record.eventid), 'success')
        return redirect(url_for("home"))

    flash_errors(form)
    return render_template('updateEvent.html', form=form, record=record)

@app.route('/api/events/<eventid>/delete', methods=['DELETE'])
def deleteEvent(eventid):
    """ deletes event """
    eventrecord =  Event.query.filter_by(eventid=eventid).first()
    if not eventrecord:
        return jsonify({'message':'This event does not exist!'})
    db.session.delete(eventrecord)
    db.session.commit()

    return jsonify({'message':'Event was deleted'})

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
