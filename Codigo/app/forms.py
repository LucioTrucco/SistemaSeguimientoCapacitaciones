from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    remember_me = BooleanField('Remember Me')


class TrainingForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    start = DateField('Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateField('Fin', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Descripcion', validators=[DataRequired()])
    comments = StringField('Comentarios')


class ClassForm(FlaskForm):
    date = DateField('Inicio', validators=[DataRequired()])
    topics = StringField('Temas vistos', validators=[DataRequired()])
    topicsNext = StringField('Temas Proxima', validators=[DataRequired()])
    comments = StringField('Comentarios')


class TrainerForm(FlaskForm):
    trainer = SelectField('trainer', validators=[DataRequired()], coerce=int)


class StudentForm(FlaskForm):
    file = IntegerField('Legajo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    surname = StringField('Apellido', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired()])
    degree = StringField('Carreras', validators=[DataRequired()])


class NewStudentForm(FlaskForm):
    file = IntegerField('Legajo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    surname = StringField('Apellido', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired()])
    degree = StringField('Carreras', validators=[DataRequired()])


class DelStudentForm(FlaskForm):
    file = IntegerField('Legajo', validators=[DataRequired()])


class UpdateStudentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    surname = StringField('Apellido', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired()])
    degree = StringField('Carreras', validators=[DataRequired()])