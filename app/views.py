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

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data:
            # Get the username and password values from the form.

            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.

            # get user id, load into session
            login_user(user)

            # remember to flash a message to the user
            return redirect(url_for("home"))  # they should be redirected to a secure-page route instead
    return render_template("login.html", form=form)

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
    

# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/api/events/<eventid>/delete', methods=['DELETE'])
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
    return user_schema.jsonify(user

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
