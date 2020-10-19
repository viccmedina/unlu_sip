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
        # Grab the user from our User Models table
        user = Usuario.query.filter_by(username=form.username.data).first()

<<<<<<< Updated upstream
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
=======
                    if next == None or not next[0]=='/':
                        next = url_for('gestion_usuario.home_admin')
                elif user.has_role('Operador'):
                    next = url_for('gestion_usuario.home_operador')
                    
                elif user.has_role('Cliente'):
                    next = url_for('gestion_usuario.home_cliente')
>>>>>>> Stashed changes

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('admin')

            return redirect(next)
    return render_template('login.html', form=form)


@gestion_usuario.route("/admin")
def admin():
    logout_user()
    return redirect(url_for('admin'))


<<<<<<< Updated upstream
@gestion_usuario.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
=======
@login_required
@gestion_usuario.route('/home_cliente', methods=['POST', 'GET'])
def home_cliente():
    """
    Vista home del usuario de tipo Cliente
    """
    return render_template('home_cliente.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='cliente')


>>>>>>> Stashed changes
