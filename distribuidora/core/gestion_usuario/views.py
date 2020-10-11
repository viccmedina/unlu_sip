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
                print('ES GERENCIA', flush=True)
                login_user(user)
                flash('Bienvenido.')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
            
                if next == None or not next[0]=='/':
                    next = url_for('admin.index')
            else:
                print('NO ES GERENCIA', flush=True)
                next = url_for('gestion_usuario.otro')

            return redirect(next)
        else:
            print('ALGO NO ESTA BIEN', flush=True)
            print(user, flush=True)
            print(user.check_password(form.password.data), flush=True)
    return render_template('login.html', form=form)

@gestion_usuario.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()    
    flash("You have been logged out.")
    return redirect(url_for('gestion_usuario.login'))

@gestion_usuario.route('/otro', methods=['POST', 'GET'])
def otro():
    return render_template('otro.html')