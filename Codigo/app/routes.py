from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import LoginForm, TrainingForm, TrainerForm, LoginForm, UserForm, ClassForm, StudentForm, SearchStudentForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Training, Class, Student, Training_students, Role
from app import db, mail
from sqlalchemy.sql.expression import func
from flask_mail import Message
from datetime import datetime
from validate_email import validate_email
from datetime import datetime, date, timedelta
import json
import re


## INICIO DE APP
@app.before_first_request
def setRoles():
    roles=["Capacitador","Admin","Direccion"]
    
    for x in roles:
        if( Role.query.filter_by(name=x).count() == 0 ):
            db.session.add(Role(name=x))
    
    db.session.commit()

#---------------------------------------------------------------------------------------------------------------
# ACCESS DENIED

@app.route('/forbidden')
def forbidden():
    if 'username' in session:
        username = session['username']
        return render_template('accessDenied.html')
    return redirect(url_for('login'))

# --------------------------------------------------------------------------------------------------------------
# INDEX

@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', title='Home')
    return redirect(url_for('login'))
    
# --------------------------------------------------------------------------------------------------------------
# LOGIN

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if len(form.username.data)==0:
            flash('El campo "username" esta vacio','error')
        elif len(form.password.data)==0:
            flash('El campo "password" esta vacio','error')
        else:
            user = User.query.filter_by(username=form.username.data).first()
            
            if user is None or not user.check_password(form.password.data):
                flash('El usuario ingreado no existe o la contrasena es incorrecta','error')
                return redirect(url_for('login'))
            session['username'] = form.username.data
            session['role'] = user.role_id
            session['idUser'] = user.id
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template(
        'login.html',
        title='Sign In',
        form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role',None)
    session.pop('idUser',None)
    logout_user()
    return redirect(url_for('login'))

# --------------------------------------------------------------------------------------------------------------
# CAPACITACIONES


@app.route('/capacitaciones')
def trainings():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'capacitaciones.html',
                title='Todas las capacitaciones',
                trainings=Training.query.all())
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/8a13')
def ochoatrece():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '8a13.html',
                title='Capacitaciones de 8 a 13',
                trainings=Training.query.filter_by(times=1))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))      


@app.route('/13a18')
def trecea18():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '13a18.html',
                title='Capacitaciones de 13 a 18',
                trainings=Training.query.filter_by(times=2))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/18a22')
def diecia22():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '18a22.html',
                title='Capacitaciones de 18 a 22',
                trainings=Training.query.filter_by(times=3))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/DDPyT')
def DDPyT():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '18a22.html',
                title='Capacitaciones DDPyT',
                trainings=Training.query.filter_by(department=1))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/DPyPP')
def DPyPP():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '18a22.html',
                title='Capacitaciones DPyPP',
                trainings=Training.query.filter_by(department=2))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/DHyA')
def DHyA():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '18a22.html',
                title='Capacitaciones DHyA',
                trainings=Training.query.filter_by(department=3))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/DeSaCo')
def DeSaCo():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                '18a22.html',
                title='Capacitaciones DeSaCo',
                trainings=Training.query.filter_by(department=4))
        else: 
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/misCapacitacionesEnCurso')
def myOngoingTrainings():
    if 'username' in session:
        username = session['username']
        idUser = session['idUser']  
        if session['role'] == 1: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'misCapacitacionesEnCurso.html',
                title='Mis capacitaciones',
                trainings=Training.query.filter_by(user_id=idUser).filter_by(finalizada=0).all())
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/misCapacitacionesFinalizadas')
def myCompletedTrainings():
    if 'username' in session:
        username = session['username']
        idUser = session['idUser']  
        if session['role'] == 1: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'misCapacitacionesFinalizadas.html',
                title='Mis capacitaciones',
                trainings=Training.query.filter_by(user_id=idUser).filter_by(finalizada=1).all())
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitacionesFinalizadas')
def completedTrainings():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'capacitacionesFinalizadas.html',
                title='Capacitaciones finalizadas',
                trainings=Training.query.filter_by(finalizada=1))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitacionesEnCurso')
def ongoingTrainings():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'capacitacionesEnCurso.html',
                title='Capacitaciones en curso',
                trainings=Training.query.filter_by(finalizada=0))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitaciones/<string:username>')
def trainings_user(username):
    if 'username' in session:
        xusername = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'capacitacionesPorUsuario.html',
                title='Capcitaciones por Usuario',
                trainings=User.query.filter_by(username=username).first().trainings)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitaciones/<int:id>')
def details(id):
    if 'username' in session:
        username = session['username']
        return render_template(
            'details.html',
            training=Training.query.get(id),
            title='Detalles')
    return redirect(url_for('login'))


@app.route('/capacitaciones/<string:id>/borrar', methods=['GET', 'POST'])
def deleteTraining(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            training = Training.query.get(id)
            db.session.delete(training)
            db.session.commit()
            flash('Capacitacion eliminada.','success')
            return redirect(url_for('trainings'))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitacionesEnCurso/<string:id>/borrar', methods=['GET', 'POST'])
def deleteOnGoingTraining(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            training = Training.query.get(id)
            db.session.delete(training)
            db.session.commit()
            flash('Capacitacion eliminada.','success')
            return redirect(url_for('ongoingTrainings'))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitacionesFinalizadas/<string:id>/borrar', methods=['GET', 'POST'])
def deleteCompletedTraining(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            training = Training.query.get(id)
            db.session.delete(training)
            db.session.commit()
            flash('Capacitacion eliminada.','success')
            return redirect(url_for('completedTrainings'))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitaciones/editar/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'username' in session:
        username = session['username']
        training = Training.query.get(id)
        form = TrainingForm(
            name=training.name,
            start=str(training.start)[:10],
            end=str(training.end)[:10],
            description=training.description,
            comments=training.comments,
            times=training.times,
            department=training.department
        )
    
        
        if request.method == 'POST':
            training.name = form.name.data
            training.start = form.start.data
            training.end = form.end.data
            #---------
            training.start=training.start.replace('/', '-') 
            training.end= training.end.replace('/','-')
            if form.times.data == '1':
                training.start=training.start+' 08:00:00'
                training.end=training.end+' 13:00:00'
            elif form.times.data == '2':
                training.start=training.start+' 13:00:00'
                training.end=training.end+' 18:00:00'
            elif form.times.data == '3':
                training.start=training.start+' 18:00:00'
                training.end=training.end+' 22:00:00'

            fechaHoy= datetime.now().date()
            xfecha = fechaHoy.strftime("%Y-%m-%d")

            fechaA = datetime.strptime(form.start.data,"%Y-%m-%d")
            fechaB = datetime.strptime(form.end.data,"%Y-%m-%d")
            fechaC = datetime.strptime(xfecha,"%Y-%m-%d")

            if fechaA > fechaB:
                flash('La fecha final debe ser posterior a la inicial','error')
            elif fechaA < fechaC:
                flash('La fecha inicial debe ser posterior o igual a la de hoy','error')
            elif fechaB < fechaC:
                flash('La fecha final debe ser posterior o igual a la de hoy','error')
            else:
                training.finalizada = False
                training.description = form.description.data
                training.comments = form.comments.data
                training.times= form.times.data
                training.department= form.department.data
                if not training.name or not training.start or not training.end or not training.description or not training.comments or not training.times or not training.department :
                    flash('Debe llenar todos los campos.','error')
                else:
                    db.session.commit()
                    flash('Capacitacion editada.','success')
                    return redirect((url_for('details', id=training.id)))
        return render_template(
            'capacitacion.html',
            title='Editar capacitacion',
            form=form)
    return redirect(url_for('login'))


@app.route('/capacitaciones/finalizar/<int:id>', methods=['GET', 'POST'])
def finish(id):
    if 'username' in session:
        username = session['username']
        training = Training.query.get(id)
        training.finalizada = True
        db.session.commit()
        flash('Capacitacion finalizada.','success')
        if session['role'] == 2 or session['role'] == 3:
            return redirect((url_for('completedTrainings')))
        else:
            return redirect((url_for('myCompletedTrainings')))
    return redirect(url_for('login'))


@app.route('/capacitaciones/crear', methods=['GET', 'POST'])
def create():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            form = TrainingForm()
            if request.method == 'POST':
                fechaStart = form.start.data
                fechaEnd= form.end.data
                fechaStart=fechaStart.replace('/', '-') 
                fechaEnd= fechaEnd.replace('/','-')

                if form.times.data == '1':
                    fechaStart=fechaStart+' 08:00:00'
                    fechaEnd=fechaEnd+' 13:00:00'
                elif form.times.data == '2':
                    fechaStart=fechaStart+' 13:00:00'
                    fechaEnd=fechaEnd+' 18:00:00'
                elif form.times.data == '3':
                    fechaStart=fechaStart+' 18:00:00'
                    fechaEnd=fechaEnd+' 22:00:00'

                fechaHoy= datetime.now().date()
                xfecha = fechaHoy.strftime("%Y/%m/%d")

                fechaA = datetime.strptime(form.start.data,"%Y/%m/%d")
                fechaB = datetime.strptime(form.end.data,"%Y/%m/%d")
                fechaC = datetime.strptime(xfecha,"%Y/%m/%d")

                if fechaA > fechaB:
                    flash('La fecha final debe ser posterior a la inicial','error')
                elif fechaA < fechaC:
                    flash('La fecha inicial debe ser posterior o igual a la de hoy','error')
                elif fechaB < fechaC:
                    flash('La fecha final debe ser posterior o igual a la de hoy','error')
                else:
                    training = Training(
                        name=form.name.data,
                        start=fechaStart,
                        end=fechaEnd,
                        finalizada=False,
                        description=form.description.data,
                        comments=form.comments.data,
                        times=form.times.data,
                        department=form.department.data
                        )

                    if not training.name: 
                        flash('El campo "Nombre" no puede estar vacio','error')
                    elif not training.start:
                        flash('El campo "Inicio" no puede estar vacio','error') 
                    elif not training.end: 
                        flash('El campo "Fin" no puede estar vacio','error')
                    elif not training.description: 
                        flash('El campo "Descripcion" no puede estar vacio','error')
                    elif not training.times: 
                        flash('El campo "Horarios" no puede estar vacio','error')
                    elif not training.department :
                        flash('El campo "Sector" no puede estar vacio','error')
                    else:    
                        db.session.add(training)
                        db.session.commit()
                        flash('Capacitacion creada.','success')
                        return redirect((url_for('select_students', id=training.id)))
            return render_template(
                'capacitacion.html',
                title='Crear capacitacion',
                form=form)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))
        



# --------------------------------------------------------------------------------------------------------------
# SEGUIMIENTO

@app.route('/capacitaciones/<int:training_id>/clases', methods=['GET', 'POST'])
def classes(training_id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 1 or session['role'] == 2: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            training=Training.query.get(training_id)
            form = ClassForm()
            if request.method == 'POST':
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
                if not new_class.date or not new_class.topics or not new_class.topicsNext:
                    flash('Debes completar todos los campos.','error')
                    return redirect((url_for('classes', training_id=training.id))) 
                else:
                    db.session.add(new_class)
                    db.session.commit()
                    flash('Clase agregada correctamente', 'success')
                    #return redirect((url_for('classes', training_id=training.id)))
            return render_template(
                'classes.html',
                title='Seguimiento',
                classes=training.classes,
                training_id=training_id,
                finalizada=training.finalizada,
                form=form)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitaciones/<int:training_id>/clases/<int:class_num>')
def class_details(training_id, class_num):
    if 'username' in session:
        username = session['username']
        training = Training.query.get(training_id)
        return render_template(
            'class_details.html',
            class_entity=training.classes.filter_by(number=class_num).first(),
            title='Detalles')
    return redirect(url_for('login'))


@app.route('/capacitaciones/<int:training_id>/clases/<int:class_num>/editar', methods=['GET', 'POST'])
def class_edit(training_id, class_num):
    if 'username' in session:
        username = session['username']
        if session['role'] == 1 or session['role'] == 2: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            training = Training.query.get(training_id)
            edit_class = training.classes.filter_by(number=class_num).first()
            form = ClassForm(date=edit_class.date,
                            topics=edit_class.topics,
                            topicsNext=edit_class.topicsNext,
                            comments=edit_class.comments)
            if request.method == 'POST':
                edit_class.date = form.date.data
                edit_class.topics = form.topics.data
                edit_class.topicsNext = form.topicsNext.data
                edit_class.comments = form.comments.data
                if not edit_class.date or not edit_class.topics or not edit_class.topicsNext or not edit_class.comments:
                    flash('Debes completar todos los campos.','error')
                else:
                    db.session.commit()
                    flash('Cambio realizado correctamente','success')
                    return redirect((url_for('classes', training_id=training.id)))
            return render_template(
                'class_edit.html',
                title='Editar clase',
                form=form)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/capacitaciones/<int:training_id>/clases/<int:class_num>/borrar', methods=['GET', 'POST'])
def class_delete(training_id, class_num):
    if 'username' in session:
        username = session['username']
        if session['role'] == 1 or session['role'] == 2: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            training = Training.query.get(training_id)
            class_entity = training.classes.filter_by(number=class_num).first()
            if(class_entity.number < len(training.classes.all())):
                next_classes = training.classes.filter(Class.number > class_num)
                for next_class in next_classes:
                    next_class.number -= 1
            db.session.delete(class_entity)
            db.session.commit()
            flash('Clase eliminada.','success')
            return redirect((url_for('classes', training_id=training.id)))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))



# --------------------------------------------------------------------------------------------------------------
# ASIGNAR CAPACITACIONES


@app.route('/asignar')
def assign():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            return render_template(
                'assign.html',
                title='Capacitaciones solicitadas',
                #trainings=Training.query.filter_by(trainer=None)
                trainings=Training.query.all())
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))
    

@app.route('/asignar/<int:id>', methods=['GET', 'POST'])
def select_trainer(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2: ##COMPROBAR SI ES ADMIN PARA ENTRAR
            form = TrainerForm()
            # TODO: Set users to avaialable users
            form.trainer.choices = [(u.id, u.username) for u in User.query.all()]
            if form.validate_on_submit():
                trainer = User.query.get(form.trainer.data)
                training = Training.query.get(id)
                training.trainer = trainer
                msg= Message('Capacitacion Asignada',
                sender='capacitacionesunla@gmail.com',
                recipients=[trainer.email])
                msg.html='<b>Capacitacion: </b>'+training.name+'<br><b>Comienza: </b>'+str(training.start)+'<br><b>Finaliza: </b>'+str(training.end)+'<br><b>Descripcion: </b>'+training.description
                mail.send(msg)
                flash('Capacitacion asignada.', 'success')
                db.session.commit()

                return redirect((url_for('details', id=training.id)))
            return render_template(
                'select_trainer.html',
                title='Asignacion',
                form=form,
                training=Training.query.get(id),
            )
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


# --------------------------------------------------------------------------------------------------------------
# USUARIOS


@app.route('/usuarios')
def users():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            return render_template(
                'users.html',
                title='Usuarios',
                users=User.query.all())
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/usuarios/crear', methods=['GET', 'POST'])
def user_create():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            form = UserForm()
            form.role.choices = [(u.id, u.name) for u in Role.query.all()]
            if request.method == 'POST':
                
                usuarios= User.query.filter_by(username=form.username.data).count()
                mails = User.query.filter_by(email=form.email.data).count()
                is_valid = validate_email(form.email.data)
                if not form.username.data: 
                        flash('El campo "Username" no puede estar vacio','error')
                elif not form.email.data: 
                    flash('El campo "Email" no puede estar vacio','error')
                elif not form.role.data: 
                    flash('El campo "Rol" no puede estar vacio','error')
                elif not form.password.data:
                    flash('El campo "Contrasena" no puede estar vacio','error')
                elif not form.confirm.data:
                    flash('El campo "Repetir Contrasena" no puede estar vacio','error')
                elif re.match(r"\W", form.username.data):
                    flash('El campo "Username" tiene caracteres invalidos','error')
                elif re.match(r"\W", form.password.data):
                    flash('El campo "Contrasena" tiene caracteres invalidos','error')
                elif re.match(r"\W", form.confirm.data):
                    flash('El campo "Repetir Contrasena" tiene caracteres invalidos','error')
                elif usuarios>0:
                    flash('Ya existe un usuario con ese nombre','error')
                elif mails>0:
                    flash('Ya existe un usuario con ese mail','error')
                elif not is_valid:
                    flash('El email ingresado es incorrecto','error')  
                elif len(form.password.data) < 4:
                    flash('Contrasena incorrecta (cantidad de caracteres mayor a 4)','error') 
                elif form.confirm.data != form.password.data:
                    flash('Las contrasenas deben coincidir','error') 
                else:
                    user = User(
                        username=form.username.data,
                        email=form.email.data,
                        role = Role.query.get(form.role.data))
                    user.set_password(form.password.data)
                    
                
                    db.session.add(user)
                    db.session.commit()
                    flash('El usuario es creado exitosamente', 'success')
                    return redirect((url_for('user_details', id=user.id)))
            return render_template(
                'user_create.html',
                title='Crear usuario',
                form=form,
                id=0)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/usuarios/<int:id>')
def user_details(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            return render_template(
                'user_details.html',
                user=User.query.get(id),
                title='Detalles del usuario')
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            user = User.query.get(id)
            form = UserForm(
                username=user.username,
                email=user.email
            )
            form.role.choices = [(u.id, u.name) for u in Role.query.all()]
            if request.method == 'POST':

                is_valid = validate_email(form.email.data)
                if not form.role.data: 
                    flash('El campo "Rol" no puede estar vacio','error')
                elif not form.password.data:
                    flash('El campo "Contrasena" no puede estar vacio','error')
                elif not form.confirm.data:
                    flash('El campo "Repetir Contrasena" no puede estar vacio','error')
                elif re.match(r"\W", form.username.data):
                    flash('El campo "Username" tiene caracteres invalidos','error')
                elif re.match(r"\W", form.password.data):
                    flash('El campo "Contrasena" tiene caracteres invalidos','error')
                elif re.match(r"\W", form.confirm.data):
                    flash('El campo "Repetir Contrasena" tiene caracteres invalidos','error')
                elif not is_valid:
                    flash('El email ingresado es incorrecto','error')  
                elif len(form.password.data) < 4:
                    flash('Contrasena incorrecta (cantidad de caracteres mayor a 4)','error') 
                elif form.confirm.data != form.password.data:
                    flash('Las contrasenas deben coincidir','error') 
                else:
                    user.username = form.username.data
                    user.email = form.email.data
                    user.Role = Role.query.get(form.role.data)
                    user.set_password(form.password.data)
                    if not user.username or not user.email or not form.password.data:
                        flash('Debes completar todos los campos.','error')
                    else:
                        db.session.commit()
                        flash('Usuario editado.', 'success')
                        return redirect((url_for('user_details', id=user.id)))
            return render_template(
                'user_create.html',
                title='Editar usuario',
                form=form,
                id=user.id)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/usuarios/borrar/<string:id>', methods=['GET', 'POST'])
def user_delete(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            flash('Usuario eliminado.','success')
            return redirect((url_for('users')))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


# --------------------------------------------------------------------------------------------------------------
# ESTUDIANTES


@app.route('/asignarEstudiante/<int:id>', methods=['GET', 'POST'])
def select_students(id):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2:
            form = SearchStudentForm()
            usedStudents = Training.query.get(id).students
            allStudents = [(u.id) for u in Student.query.all()]
            list1 = []
            
            for x in usedStudents:
                list1.append(x.id)

            list3= [item for item in allStudents if item not in list1]

            xchoices=[]

            for x in range(len(list3)-1,-1,-1):
                xchoices.extend([(u.id, u.name) for u in Student.query.filter_by(id=list3[x])])
            
            form.search.choices=xchoices
            
            if form.validate_on_submit():
                xstudents=form.search.data
                for xid in xstudents:
                    student = Student.query.get(xid)
                    student.lstTraining.append(Training.query.get(id))
                    training=Training.query.get(id)
                    #ENVIAR MAIL A ESTUDIANTE
                    msg= Message('Capacitacion Asignada',
                    sender='seguimientounlatest@gmail.com',
                    recipients=[student.email])
                    msg.html='<b>Capacitacion: </b>'+training.name+'<br><b>Comienza: </b>'+str(training.start)+'<br><b>Finaliza: </b>'+str(training.end)+'<br><b>Descripcion: </b>'+training.description
                    mail.send(msg)
                    db.session.commit()
                    flash('Estudiantes asignados. Les llegara un mail con informacion sobre la capacitacion.','success')
                return redirect((url_for('trainings')))
            return render_template(
                'select_students.html',
                title='Asignacion',
                form=form,
                training=Training.query.get(id),
                students=Student.query.all(),
                list=form.search.choices
            )
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/alumnos/agregar', methods=['GET', 'POST'])
def student_create():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2:
            form = StudentForm()
            if request.method == 'POST':
                
                if form.file.data <=0:
                    flash('El legajo debe ser mayor a cero','error')
                elif form.file.data > 2147483647:
                    flash('El numero de legajo debe ser menor.','error')
                else:
                    estudiante = Student.query.filter_by(file=form.file.data).count()
                    mail = Student.query.filter_by(email=form.email.data).count()
                    is_valid = validate_email(form.email.data)

                    if estudiante > 0:
                        flash('Ya existe un estudiante con el mismo legajo.','error')
                    elif mail > 0:
                        flash('Ya existe un estudiante con el mismo email.','error')
                    elif not is_valid:
                        flash('El campo "Email" contiene caracteres invalidos','error')
                    elif re.match(r"\W", form.surname.data):
                        flash('El campo "Apellido" tiene caracteres invalidos','error')
                    elif re.match(r"\W", form.name.data):
                        flash('El campo "Nombre" tiene caracteres invalidos','error')
                    elif re.match(r"\W", form.degree.data):
                        flash('El campo "Carrera" tiene caracteres invalidos','error')
                    else:
                        student = Student(
                            file=form.file.data,
                            email=form.email.data,
                            surname=form.surname.data,
                            name=form.name.data,
                            degree=form.degree.data)
                        if not student.file or not student.email or not student.surname or not student.name or not student.degree:
                            flash('Debes completar todos los campos.','error')
                        else:
                            db.session.add(student)
                            db.session.commit()
                            flash('Estudiante agregado.','success')
                            return redirect(url_for('students'))
            return render_template(
                'student_create.html',
                title='Crear estudiante',
                form=form)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/alumnos/<string:file>/borrar', methods=['GET', 'POST'])
def student_delete(file):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2:
            student = Student.query.filter_by(file=file).first()
            db.session.delete(student)
            db.session.commit()
            flash('Estudiante eliminado','success')
            return redirect(url_for('students'))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/alumnos/<int:file>/editar', methods=['GET', 'POST'])
def student_edit(file):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2:
            student = Student.query.filter_by(file=file).first()
            form = StudentForm(
                file=student.file,
                name=student.name,
                surname=student.surname,
                email=student.email,
                degree=student.degree
            )   
            if request.method == 'POST':
                if form.file.data <=0:
                    flash('El legajo debe ser mayor a cero','error')
                elif form.file.data > 2147483647:
                    flash('El numero de legajo debe ser menor.','error')
                else:
                    is_valid = validate_email(form.email.data)

                    if not is_valid:
                        flash('El campo "Email" contiene caracteres invalidos','error')
                    elif re.match(r"\W", form.surname.data):
                        flash('El campo "Apellido" tiene caracteres invalidos','error')
                    elif re.match(r"\W", form.name.data):
                        flash('El campo "Nombre" tiene caracteres invalidos','error')
                    elif re.match(r"\W", form.degree.data):
                        flash('El campo "Carrera" tiene caracteres invalidos','error')
                    else:
                        student.name=form.name.data
                        student.surname=form.surname.data
                        student.email=form.email.data
                        student.degree=form.degree.data
                        if not student.file or not student.email or not student.surname or not student.name or not student.degree:
                            flash('Debes completar todos los campos.','error')
                        else:
                            db.session.commit()
                            flash('Estudiante editado.','success')
                            return redirect(url_for('students'))
            return render_template('student_create.html', title='Actualizar Estudiante',
                                    form=form)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/alumnos/buscar', methods=['GET', 'POST'])
def searchStudent():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2:
            form = SearchStudentForm()
            if form.validate_on_submit():
                file = form.search.data
                return redirect((url_for('student_details.html', file=file)))
            return render_template('student_search.html', title='Buscar Estudiante', form=form)
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/alumnos/<int:file>', methods=['GET', 'POST'])
def student_detials(file):
    if 'username' in session:
        username = session['username']
        if session['role'] == 2:
            return render_template('detailStudent.html', title='Detalles de Estudiante',
                                    student=Student.query.filter_by(file=file))
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


@app.route('/alumnos')
def students():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            return render_template(
                'students.html',
                title='Todos los estudiantes',
                students= Student.query.all())
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))


# --------------------------------------------------------------------------------------------------------------
#ESTADISTICAS

@app.route('/estadisticas')
def estadisticas():
    if 'username' in session:
        username = session['username']
        if session['role'] == 2 or session['role'] == 3:
            #variables
            cantCursando=0
            cantEstudiantes=0
            cantNoCursando=0
            cantCapacitando=0
            cantCapacitadores=0
            cantNoCapacitando=0

            #Stats Capacitaciones
            statsCapacitaciones=[Training.query.filter_by(finalizada=1).count(), Training.query.filter_by(finalizada=0).count() ]
            
            #Stats Estudiantes
            queryCursando = db.session.query(Student.id.distinct()).join(Training_students, Student.id == Training_students.c.student_id).join(Training, Training_students.c.training_id == Training.id).filter(Training.finalizada==0).all()
            queryEstudiantes = db.session.query(Student.id).all()
            
            for result in queryCursando:
                cantCursando+=1
            
            for result in queryEstudiantes:
                cantEstudiantes+=1
            
            cantNoCursando=cantEstudiantes-cantCursando

            statsEstudiantes = [cantCursando, cantNoCursando]
            
            #Stats Capacitadores
            queryCapacitando = db.session.query(User.id.distinct()).join(Training, User.id == Training.user_id).filter(Training.finalizada==0).filter(User.role_id!=2).all()
            queryCapacitadores = db.session.query(User.id).filter(User.role_id!=2).all()
            
            for result in queryCapacitando:
                cantCapacitando+=1


            for result in queryCapacitadores:
                cantCapacitadores+=1
            
            cantNoCapacitando=cantCapacitadores-cantCapacitando

            statsCapacitadores = [cantCapacitando, cantNoCapacitando]

            #Stats capacitaciones por horario
            canth1 = Training.query.filter_by(times=1).count()
            canth2 = Training.query.filter_by(times=2).count()
            canth3 = Training.query.filter_by(times=3).count()

            statsCapacitacionesTime=[canth1,canth2,canth3]

            #Stats capacitaciones por sector
            cants1 = Training.query.filter_by(department=1).count()
            cants2 = Training.query.filter_by(department=2).count()
            cants3 = Training.query.filter_by(department=3).count()
            cants4 = Training.query.filter_by(department=4).count()

            statsCapacitacionesDpto=[cants1,cants2,cants3,cants4]

            return render_template(
                'estadisticas.html',
                title='Estadisticas',
                statsCapacitaciones=map(json.dumps,statsCapacitaciones),
                statsEstudiantes= map(json.dumps,statsEstudiantes),
                statsCapacitadores=map(json.dumps, statsCapacitadores),
                statsCapacitacionesTime=map(json.dumps, statsCapacitacionesTime),
                statsCapacitacionesDpto=map(json.dumps, statsCapacitacionesDpto)
            )
        else:
            return redirect(url_for('forbidden'))
    return redirect(url_for('login'))