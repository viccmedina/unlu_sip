from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from werkzeug.security import generate_password_hash,check_password_hash
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.gestion_usuario.forms import LoginForm

gestion_usuario = Blueprint('gestion_usuario', __name__, template_folder='templates')

@gestion_usuario.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = Usuario.query.filter_by(username=form.username.data).first()
        print('el usuario tiene el rol: {}'.format(user.usuario_rol), flush=True)
        if user.check_password(form.password.data) and user is not None:
            print('pass y username OK', flush=True)
            #Log in the user
            if user.has_role('Gerencia'):
                login_user(user)
                flash('Bienvenido.')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
            
                if next == None or not next[0]=='/':
                    next = url_for('admin.index')
            elif user.has_role('Operador'):
                next = url_for('gestion_usuario.home_operador')
                
            elif user.has_role('Cliente'):
                flash('Bienvenido.')
                next = url_for('gestion_usuario.home_cliente')

            login_user(user)
            flash('Bienvenido.') 
            return redirect(next)
        else:
            print('ALGO NO ESTA BIEN', flush=True)
            print(user, flush=True)
            print(user.check_password(form.password.data), flush=True)

    return render_template('login.html', form=form)


@login_required
@gestion_usuario.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()    
    flash("You have been logged out.")
    return redirect(url_for('gestion_usuario.login'))


@login_required
@gestion_usuario.route('/home_operador', methods=['POST', 'GET'])
def home_operador():
    return render_template('home_operador.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated)


@login_required
@gestion_usuario.route('/home_cliente', methods=['POST', 'GET'])
def home_cliente():
    return render_template('home_cliente.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated)
