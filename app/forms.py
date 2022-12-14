from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddItem(FlaskForm):
    name_item = StringField('Item Name', validators=[DataRequired()])
    name_body = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteItem(FlaskForm):
    choices = ['Delete All']
    select = SelectField('Select Item', validators=[DataRequired()], choices=choices)
    submit = SubmitField('Submit')


class HelpUser(FlaskForm):
    otdel = SelectField('Where to send the question?', validators=[DataRequired()], choices=[
        "Technical support",
        "Director's mail"
    ])
    question = StringField('Ask your question', validators=[DataRequired()])
    submit = SubmitField('Submit')
