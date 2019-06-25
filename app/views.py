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

@app.route("/api/users/register",  methods=["GET","POST"]) # added GET for testing purposes
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        telnum = form.telnum.data
        email = form.email.data
            
        #date_created = datetime.datetime.now().strftime("%B %d, %Y")
        
        new_user = EventManager(username=username,password=password,first_name=firstname, last_name=lastname, 
                             telnum=telnum, email=email)
            
        db.session.add(new_user)
        db.session.commit()
        
        flash('User added', 'success')
        return redirect(url_for("home")) # Where should it go after the user is created ?
    return render_template('register.html', form=form)

@app.route("/api/events/createEvent",  methods=["GET","POST"]) # added GET for testing purposes
def createNewEvent():
    form = EventForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        title = form.title.data
        category = form.category.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        description= form.description.data 
        cost = form.cost.data
        venue = form.venue.data
        flyer = form.flyer.data
            
        #date_created = datetime.datetime.now().strftime("%B %d, %Y")
        
        new_user = Event(name=name,title=title,category=category, start_date=start_date, end_date=end_date,
                             description=description, cost=cost, venue=venue, flyer=flyer)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Event added', 'success')
        return redirect(url_for("home")) # Where should it go after the user is created ?
    return render_template('newevent.html', form=form)

@app.route('/api/events/<eventid>/viewEventInfo', methods=['GET'])
def viewEventInfo(eventid):
    """Render details of particular event."""
    result =Event.query.filter_by(eventid=eventid).first()
    
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

@app.route('/api/events/<eventid>/delete', methods=['GET'])
def deleteEvent(eventid):
    """ deletes event """
    eventrecord =  Event.query.filter_by(eventid=eventid).first()
    db.session.delete(eventrecord)
    db.session.commit()
    flash('You have successfully deleted the event', 'success')
    
    return redirect(url_for('home'))

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
