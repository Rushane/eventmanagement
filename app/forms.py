from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, TextField, SelectField, validators, DateTimeField, FloatField
from wtforms.validators import InputRequired, Email, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = TextField('First Name', validators=[DataRequired()])
    last_name = TextField('Last Name', validators=[DataRequired()])
    telnum = TextField('Telephone number', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()])

class EventForm(FlaskForm):
    name = TextField('Event Name', validators=[DataRequired()])
    title = TextField('Title', validators=[DataRequired()])
    category = TextField('Category', validators=[DataRequired()]) # should be select field possibly
    start_date = DateTimeField('Start Date', format="%Y-%m-%d  %H:%M")
    end_date = DateTimeField('End Date', format="%Y-%m-%d  %H:%M")
    description= TextAreaField('Description', validators=[validators.Optional()])
    cost = FloatField('Cost',validators=[DataRequired()])
    venue = TextField('Venue', validators=[DataRequired()])
    flyer = TextField('Flyer', validators=[DataRequired()])