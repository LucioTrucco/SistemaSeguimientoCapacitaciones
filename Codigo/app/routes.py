from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, TrainingForm, TrainerForm, LoginForm, UserForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Training
from app import db

# --------------------------------------------------------------------------------------------------------------


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
# --------------------------------------------------------------------------------------------------------------
# LOGIN


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

# --------------------------------------------------------------------------------------------------------------
# CAPACITACIONES


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


@app.route('/capacitaciones/editar/<int:id>', methods=['GET', 'POST'])
def edit(id):
    training = Training.query.get(id)
    form = TrainingForm(
        name=training.name,
        start=training.start,
        end=training.end,
        description=training.description,
        comments=training.comments,
    )
    if form.validate_on_submit():
        training.name = form.name.data
        training.start = form.start.data
        training.end = form.end.data
        training.finalizada = False
        training.description = form.description.data
        training.comments = form.comments.data
        db.session.commit()
        return redirect((url_for('details', id=training.id)))
    return render_template(
        'capacitacion.html',
        title='Editar capacitacion',
        form=form)


@app.route('/capacitaciones/finalizar/<int:id>', methods=['GET', 'POST'])
def finish(id):
    training = Training.query.get(id)
    training.finalizada = True
    db.session.commit()
    return redirect((url_for('details', id=training.id)))


@app.route('/capacitaciones/crear', methods=['GET', 'POST'])
def create():
    form = TrainingForm()
    if form.validate_on_submit():
        training = Training(
            name=form.name.data,
            start=form.start.data,
            end=form.end.data,
            finalizada=False,
            description=form.description.data,
            comments=form.comments.data)
        db.session.add(training)
        db.session.commit()
        return redirect((url_for('details', id=training.id)))
    return render_template(
        'capacitacion.html',
        title='Crear capacitacion',
        form=form)


# --------------------------------------------------------------------------------------------------------------
# ASIGNAR CAPACITACIONES


@app.route('/asignar')
def assign():
    return render_template(
        'assign.html',
        title='Capacitaciones solicitadas',
        trainings=Training.query.filter_by(trainer=None)
    )


@app.route('/asignar/<int:id>', methods=['GET', 'POST'])
def select_trainer(id):
    form = TrainerForm()
    # TODO: Set users to avaialable users
    form.trainer.choices = [(u.id, u.username) for u in User.query.all()]
    if form.validate_on_submit():
        trainer = User.query.get(form.trainer.data)
        training = Training.query.get(id)
        training.trainer = trainer
        db.session.commit()
        return redirect((url_for('details', id=training.id)))
    return render_template(
        'select_trainer.html',
        title='Asignacion',
        form=form,
        training=Training.query.get(id),
    )

# --------------------------------------------------------------------------------------------------------------
# USUARIOS

@app.route('/usuarios')
def users():
    return render_template(
        'users.html',
        title='Usuarios',
        users=User.query.all())


@app.route('/usuarios/crear', methods=['GET', 'POST'])
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect((url_for('user_details', id=user.id)))
    return render_template(
        'user_create.html',
        title='Crear usuario',
        form=form)


@app.route('/usuarios/<int:id>')
def user_details(id):
    return render_template(
        'user_details.html',
        user=User.query.get(id),
        title='Detalles del usuario')


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
    user = User.query.get(id)
    form = UserForm(
        username=user.username,
        email=user.email,
    )
    if form.validate_on_submit():
        user.username=form.username.data
        user.email=form.email.data
        if(form.password.data is not None and form.data.password != ''):
            user.set_password(form.password.data)
        db.session.commit()
        return redirect((url_for('user_details', id=user.id)))
    return render_template(
        'user_create.html',
        title='Crear usuario',
        form=form)


@app.route('/usuarios/borrar/<int:id>', methods=['GET', 'POST'])
def user_delete(id):
    if request.method == 'POST':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return redirect((url_for('users')))
    return render_template(
        'user_delete.html',
        title='Borrar usuario',
        user=User.query.get(id))