from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from wtforms.fields.html5 import DateField
from app.models import User
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateTour(FlaskForm):
    tour_name = StringField('Tour Name', validators=[DataRequired()])
    tour_description = TextAreaField('Description', validators=[DataRequired()])
    tour_location = StringField('Location', validators=[DataRequired()])
    tour_price = FloatField('Price', validators=[Optional()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    submit = SubmitField('Publish')
    
    def validate(self):
        result = super(CreateTour, self).validate()
        if (self.start_date.data > self.end_date.data):
            return False
        else:
            return result
