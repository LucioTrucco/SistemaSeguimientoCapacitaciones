from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    remember_me = BooleanField('Remember Me')


class TrainingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start = DateField('Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateField('Fin', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Descripcion', validators=[DataRequired()])


class ClassForm(FlaskForm):
    date = DateField('Inicio', validators=[DataRequired()])
    topics = StringField('Name', validators=[DataRequired()])
    topicsNext = StringField('Name', validators=[DataRequired()])
    comments = StringField('Name', validators=[DataRequired()])
