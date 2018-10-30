from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, TrainingForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Training
from app import db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template(
        'login.html',
        title='Sign In',
        form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/capacitaciones')
def trainings():
    return render_template(
        'capacitaciones.html',
        title='Todas las capacitaciones',
        trainings=Training.query.all())


@app.route('/capacitaciones/<string:username>')
def trainings_user(username):
    return render_template(
        'capacitaciones.html',
        title='Capcitaciones en Curso',
        trainings=User.query.filter_by(username=username).first().trainings)


@app.route('/capacitaciones/<int:id>')
def details(id):
    return render_template(
        'details.html',
        training=Training.query.get(id),
        title='Detalles')


@app.route('/capacitaciones/crear', methods=['GET', 'POST'])
def create():
    form = TrainingForm()
    # pdb.set_trace()
    if form.validate_on_submit():
        training = Training(
            name=form.name.data,
            start=form.start.data,
            end=form.end.data,
            finalizada=False,
            description=form.description.data)
        db.session.add(training)
        db.session.commit()
        return redirect((url_for('details', id=training.id)))
    return render_template(
        'capacitacion.html',
        title='Crear capacitacion',
        form=form)


@app.route('/users')
def users():
    return render_template(
        'users.html',
        title='Usuarios',
        users=User.query.all())


@app.route('/assign')
def assign():
    return render_template(
        'assign.html',
        title='Capacitaciones solicitadas',
        trainings=Training.query.filter_by(trainer=None)
    )


@app.route('/assign/<int:id>')
def select_trainer(id):
    return render_template(
        'select_trainer.html',
        title='Asignacion',
        training=Training.query.get(id),
        available_users=User.query.all()
    )