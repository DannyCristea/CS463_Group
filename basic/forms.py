from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField,
                      RadioField, SelectField, TextField, TextAreaField, PasswordField)

from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from basic.models import User

class ContactForm(FlaskForm):

    name = StringField('Name:',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:',  validators=[DataRequired(), Email()])
    comment = TextAreaField()
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    username = StringField('Username: ',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:',  validators=[DataRequired(), Email()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    #validation to check user don't sign up with same username
    def validate_username(self, username):
        #username.data backs from the form and first backs from the database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken, Please choose a new one.')

        #validation to check user don't sign up with same email
    def validate_email(self, email):
        #email.data backs from the form and first backs from the database
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken, Please choose a new one.')


class LoginForm(FlaskForm):

    email = StringField('Email: ',  validators=[DataRequired(), Email()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email:',  validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    #validate that the user have an account with us
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email, you should sign up first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password: ',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')
    
