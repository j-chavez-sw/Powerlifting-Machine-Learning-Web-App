from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from Capstone.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is in use already')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is in use already')

class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired()])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is in use already')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is in use already')

class BenchForm(FlaskForm):

    equipment = RadioField(label='Equipment',choices=[(0,'Raw'),(2,'Wrap'),(1,'Singe-Ply'),
                                                      (3,'Multi-Ply')], validators=[InputRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex',choices=[(1,'Male'),(0,'Female')], validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    squat = IntegerField('Squat - in KG', validators=[DataRequired()])
    deadlift = IntegerField('Deadlift - in KG', validators=[DataRequired()])
    submit = SubmitField('Update')

class DeadliftForm(FlaskForm):

    equipment = RadioField(label='Equipment',choices=[(0,'Raw'),(2,'Wrap'),(1,'Singe-Ply'),
                                                      (3,'Multi-Ply')], validators=[InputRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex',choices=[(1,'Male'),(0,'Female')], validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    bench = IntegerField('Bench - in KG', validators=[DataRequired()])
    squat = IntegerField('Squat - in KG', validators=[DataRequired()])
    submit = SubmitField('Update')

class SquatForm(FlaskForm):

    equipment = RadioField(label='Equipment',choices=[(0,'Raw'),(2,'Wrap'),(1,'Singe-Ply'),
                                                      (3,'Multi-Ply')], validators=[InputRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex',choices=[(1,'Male'),(0,'Female')], validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    bench = IntegerField('Bench - in KG', validators=[DataRequired()])
    deadlift = IntegerField('Deadlift - in KG', validators=[DataRequired()])
    submit = SubmitField('Update')


