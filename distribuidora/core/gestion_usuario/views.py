from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from werkzeug.security import generate_password_hash,check_password_hash
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.gestion_usuario.forms import LoginForm,CambiarContraseña,CambiarContraseñaLogin
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora.core.gestion_usuario.query import *
from distribuidora.core.gestion_usuario.helper import updateContraseña

gestion_usuario = Blueprint('gestion_usuario', __name__, template_folder='templates')

@gestion_usuario.route('/login', methods=['GET', 'POST'])
def login():
    """
    Validamos el formulario de logue. Tenemos en cuenta si el usuario existe
    en nuestro sistema, también si la password es la correcta.
    Dependiendo de su rol, el usuario en cuestión es redireccionado a su propio
    home.
    """
    form = LoginForm()
    if form.validate_on_submit():

        user = Usuario.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                print('pass y username OK', flush=True)
                #Log in the user
                if user.has_role('Gerencia'):
                    login_user(user)
                    next = request.args.get('next')

                    if next == None or not next[0]=='/':
                        next = url_for('admin.index')
                elif user.has_role('Operador'):
                    next = url_for('gestion_usuario.home_operador')

                elif user.has_role('Cliente'):
                    next = url_for('gestion_usuario.home_cliente')

                login_user(user)
                return redirect(next)
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash(u'Usuario inexistente', 'error')

    return render_template('login.html', form=form)


@login_required
@gestion_usuario.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Para cerrar sesión.
    """
    logout_user()
    flash("Usted ha cerrado sesión", 'warning')
    return redirect(url_for('gestion_usuario.login'))


@login_required
@gestion_usuario.route('/home_operador', methods=['POST', 'GET'])
def home_operador():
    """
    Vista home del usuario de tipo Operador
    """
    site = 'Home {}'.format(current_user.get_username())
    return render_template('home_operador.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador',\
        site=site,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))


@login_required
@gestion_usuario.route('/home_cliente', methods=['POST', 'GET'])
def home_cliente():
    """
    Vista home del usuario de tipo Cliente
    """
    site = 'Home {}'.format(current_user.get_username())
    return render_template('home_cliente.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='cliente',\
        site=site,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))


@login_required
@gestion_usuario.route('/cambiar_contraseña', methods=['POST', 'GET'])
def cambiar_contraseña():
    """
    Vista home del usuario de tipo Cliente
    """

    b = request.args.get('b')
    if not b:
        form = CambiarContraseña()
        site = 'Home {}'.format(current_user.get_username())
        if form.validate_on_submit():
            passOld = form.passwordAnt.data
            passNew = form.passwordNew.data
            passConfNew = form.passwordConfNew.data
            if passNew != passConfNew:
                flash("ERROR, Las contraseñas ingresadas no coinciden",'error')
            else:
                user = Usuario.query.filter_by(username=current_user.get_username()).first()
                if user.check_password(passOld):
                    password_hash = generate_password_hash(passConfNew)
                    #updateContraseña(password_hash,current_user.get_username())
                    db.engine.execute(UPDATE_USER.format(passw=password_hash,user=current_user.get_username()))
                    flash("Se ha cambiado la contraseña correctamente",'warning')
                else:
                    flash("La clave ingresada es incorrecta",'error')
    else:
        form = CambiarContraseñaLogin()
        if form.validate_on_submit():
            users = form.username.data
            passOld = form.passwordAnt.data
            passNew = form.passwordNew.data
            passConfNew = form.passwordConfNew.data
            if passNew != passConfNew:
                flash("ERROR, Las contraseñas ingresadas no coinciden",'error')
            else:
                user = Usuario.query.filter_by(username=users).first()
                if user.check_password(passOld):
                    password_hash = generate_password_hash(passConfNew)
                    #updateContraseña(password_hash,current_user.get_username())
                    print("user {}".format(users))
                    db.engine.execute(UPDATE_USER.format(passw=password_hash,user=users))
                    flash("Se ha cambiado la contraseña correctamente",'warning')
                else:
                    flash("La clave ingresada es incorrecta",'error')

        return render_template('cambiar_contraseña_login.html', \
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
            form=form)

    return render_template('cambiar_contraseña.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='cliente',\
        site=site,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        form=form)
