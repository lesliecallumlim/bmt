from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, FloatField
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
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    description = TextAreaField('Description', validators=[Optional()])
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
    # def __init__(self, _start_date = None, _end_date = None, *args, **kwargs):
        # super(CreateTour, self).__init__(*args, **kwargs)
        # self._start_date = self.start_date.data
        # self._end_date = self.end_date.data

    
    # Dates that are invalid are automatically rejected
    # def validate(self):
        # if (self._start_date > self._end_date):
            # raise ValidationError('Please enter a start date that is earlier than the end date!')

class EditProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    description = TextAreaField('Description')
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Submit')

    # Basically what the entailing functions does is that it overrides the default init method 
    # with a series of additional parameters that receives the current username and
    # the email. With that, we prevent users from changing to email/user that is the same
    # to that of the another user.
    def __init__(self, curr_username, curr_email, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.curr_username = curr_username
        self.curr_email = curr_email

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None and username.data != self.curr_username:
            raise ValidationError('Please use a different username.')  

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and email.data != self.curr_email:
            raise ValidationError('Please use a different email.')   

class FeedbackForm(FlaskForm):
    tour_feedback = TextAreaField('What do you think?',validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('search', [DataRequired()])
    _choice = [('Tour Name', 'Tour Name'), ('Location', 'Location'), ('Max Price', 'Max Price')]
    choice = SelectField('type', choices = _choice)
    submit = SubmitField('Search')

    # def validate(self):
    #     result = super(SearchForm, self).validate()
    #     if self.choice == ('Max Price', 'Max Price'):
    #         try:
    #             f = float(self.search)
    #         except:
    #             raise ValidationError('Please enter a valid value!')
    #     else:
    #         return result