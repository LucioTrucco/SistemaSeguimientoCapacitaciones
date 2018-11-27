from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, TrainingForm, TrainerForm, LoginForm, UserForm, ClassForm, StudentForm, SearchStudentForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Training, Class, Student
from app import db, mail
from sqlalchemy.sql.expression import func
from flask_mail import Message
from datetime import datetime

# --------------------------------------------------------------------------------------------------------------
# INDEX


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
            comments=form.comments.data
            )
        db.session.add(training)
        db.session.commit()
        return redirect((url_for('select_students', id=training.id)))
    return render_template(
        'capacitacion.html',
        title='Crear capacitacion',
        form=form)


# --------------------------------------------------------------------------------------------------------------
# SEGUIMIENTO

@app.route('/capacitaciones/<int:training_id>/clases')
def classes(training_id):
    training=Training.query.get(training_id)
    return render_template(
        'classes.html',
        title='Seguimiento',
        classes=training.classes,
        training_id=training_id,
        finalizada=training.finalizada)


@app.route('/capacitaciones/<int:training_id>/clases/agregar', methods=['GET', 'POST'])
def class_create(training_id):
    training = Training.query.get(training_id)
    form = ClassForm()
    if form.validate_on_submit():
        new_class = Class(
            date=form.date.data,
            topics=form.topics.data,
            topicsNext=form.topicsNext.data,
            comments=form.comments.data)
        if len(training.classes.all()) == 0:
            new_class.number = 1
        else:
            new_class.number = db.session.query(func.max(Class.number)).filter(
                Class.training_id == training_id).first()[0] + 1
        new_class.training = training
        db.session.add(new_class)
        db.session.commit()
        return redirect((url_for('classes', training_id=training.id)))
    return render_template(
        'class_create.html',
        title='Crear clase',
        form=form)


@app.route('/capacitaciones/<int:training_id>/clases/<int:class_num>')
def class_details(training_id, class_num):
    training = Training.query.get(training_id)
    return render_template(
        'class_details.html',
        class_entity=training.classes.filter_by(number=class_num).first(),
        title='Detalles')


@app.route('/capacitaciones/<int:training_id>/clases/<int:class_num>/editar', methods=['GET', 'POST'])
def class_edit(training_id, class_num):
    training = Training.query.get(training_id)
    edit_class = training.classes.filter_by(number=class_num).first()
    form = ClassForm(date=edit_class.date,
                     topics=edit_class.topics,
                     topicsNext=edit_class.topicsNext,
                     comments=edit_class.comments)
    if form.validate_on_submit():
        edit_class.date = form.date.data
        edit_class.topics = form.topics.data
        edit_class.topicsNext = form.topicsNext.data
        edit_class.comments = form.comments.data
        db.session.commit()
        return redirect((url_for('classes', training_id=training.id)))
    return render_template(
        'class_create.html',
        title='Editar clase',
        form=form)


@app.route('/capacitaciones/<int:training_id>/clases/<int:class_num>/borrar', methods=['GET', 'POST'])
def class_delete(training_id, class_num):
    training = Training.query.get(training_id)
    class_entity = training.classes.filter_by(number=class_num).first()
    if request.method == 'POST':
        if(class_entity.number < len(training.classes.all())):
            next_classes = training.classes.filter(Class.number > class_num)
            for next_class in next_classes:
                next_class.number -= 1
        db.session.delete(class_entity)
        db.session.commit()
        return redirect((url_for('classes', training_id=training.id)))
    return render_template(
        'class_delete.html',
        title='Borrar clase',
        training_id=training_id,
        class_entity=class_entity)




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
        msg= Message('Capacitacion Asignada',
        sender='matiastorsello@gmail.com',
        recipients=[trainer.email])
        msg.add_recipient('trucco.lucioj@gmail.com')
        msg.html='<b>Capacitacion: </b>'+training.name+'<br><b>Comienza: </b>'+str(training.start)+'<br><b>Finaliza: </b>'+str(training.end)+'<br><b>Descripcion: </b>'+training.description
        mail.send(msg)
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
        user.username = form.username.data
        user.email = form.email.data
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


# ESTUDIANTES


@app.route('/asignarEstudiante/<int:id>', methods=['GET', 'POST'])
def select_students(id):
    form = SearchStudentForm()
    # TODO: Set users to avaialable users
    form.search.choices = [(u.id, u.name) for u in Student.query.all()]

    if form.validate_on_submit():
        for xid, name in form.search.choices:
            student = Student.query.get(xid)
            student.lstTraining.append(Training.query.get(id))
            db.session.commit()
        return redirect((url_for('index')))
    return render_template(
        'select_students.html',
        title='Asignacion',
        form=form,
        training=Training.query.get(id),
    )


@app.route('/alumnos/agregar', methods=['GET', 'POST'])
def student_create():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            file=form.file.data,
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            degree=form.degree.data)
        db.session.add(student)
        db.session.commit()
        flash('Estudiante creado', 'success')
        return redirect(url_for('index'))
    return render_template(
        'student_create.html',
        title='Crear estudiante',
        form=form)


@app.route('/alumnos/<int:file>/borrar', methods=['GET', 'POST'])
def student_delete(file):
    student = Student.query.filter_by(file=file)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        return redirect((url_for('students')))
    return render_template(
        'student_delete.html',
        title='Borrar estudiante',
        student=student) 


@app.route('/alumnos/<int:file>/editar', methods=['GET', 'POST'])
def student_edit(file):
    student = Student.query.filter_by(file=file).first()
    form = StudentForm(
        file=student.file,
        name=student.name,
        surname=student.surname,
        email=student.email,
        degree=student.degree
    )   
    if form.validate_on_submit():
        student.name=form.name.data
        student.surname=form.surname.data
        student.email=form.email.data
        student.degree=form.degree.data
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('student_create.html', title='Actualizar Estudiante',
                            form=form)


@app.route('/alumnos/buscar', methods=['GET', 'POST'])
def searchStudent():
    form = SearchStudentForm()
    if form.validate_on_submit():
        file = form.search.data
        return redirect((url_for('student_details.html', file=file)))
    return render_template('student_search.html', title='Buscar Estudiante', form=form)


@app.route('/alumnos/<int:file>', methods=['GET', 'POST'])
def student_detials(file):
    return render_template('detailStudent.html', title='Detalles de Estudiante',
                            student=Student.query.filter_by(file=file))


@app.route('/alumnos')
def students():
    return render_template(
        'students.html',
        title='Todos los estudiantes',
        students= Student.query.all())

        