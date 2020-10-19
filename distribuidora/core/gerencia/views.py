from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from werkzeug.security import generate_password_hash, check_password_hash
import xlsxwriter as xw
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.gestion_usuario.forms import LoginForm
from distribuidora.models.precio import Precio
from distribuidora.models.producto import Producto

gestion_admin = Blueprint('gestion_admin', __name__, template_folder='templates')


@gestion_admin.route('/gerencia', methods=['GET', 'POST'])
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
                # Log in the user
                if user.has_role('Gerencia'):
                    login_user(user)
                    next = request.args.get('next')

                    if next == None or not next[0] == '/':
                        next = url_for('gestion_admin.home_admin')
                elif user.has_role('Operador'):
                    next = url_for('gestion_admin.home_operador')

                elif user.has_role('Cliente'):
                    next = url_for('gestion_admin.home_cliente')

                login_user(user)
                return redirect(next)
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash(u'Usuario inexistente', 'error')

    return render_template('login.html', form=form)


@login_required
@gestion_admin.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Para cerrar sesión.
    """
    logout_user()
    flash("Usted ha cerrador sesión", 'warning')
    return redirect(url_for('gestion_usuario.login'))


@login_required
@gestion_admin.route('/home_admin', methods=['POST', 'GET'])
def home_admin():
    """
    Vista home del usuario de tipo Admin
    """
    return render_template('home_admin.html', \
                           datos=current_user.get_mis_datos(), \
                           is_authenticated=current_user.is_authenticated, \
                           rol='Gerencia')


@gestion_admin.route('/informes', methods=['POST', 'GET'])
def informes():
    """
    Vista home del usuario de tipo Admin
    """
    print("entro en informes")
    return render_template('informes.html', \
                           datos=current_user.get_mis_datos(), \
                           is_authenticated=current_user.is_authenticated, \
                           rol='Gerencia')



@gestion_admin.route('/list_precios', methods=['POST', 'GET'])
def emitir_lista_precios():
    print("vino a escribir")
    workbook = xw.Workbook('lista_precios.xlsx')
    lista_precios = workbook.add_worksheet(name="lista_precios")
    row = 0
    col = 0
    id = 1
    producto = Producto.query.filter_by(producto_id=id).first()
    while producto is not None:
        print(producto)
        print("es none chabooon")
        precio = Precio.query.filter_by(precio_id=producto.precio_id).first()
        print(producto.descripcion)
        print(precio.valor)
        lista_precios.write(row, col, producto.descripcion)
        lista_precios.write(row, col + 1, precio.valor)
        row = row + 1
        id = id + 1
        producto = Producto.query.filter_by(producto_id=id).first()


    print("creando archivo")
    workbook.close()
    return render_template('informes.html', \
                           datos=current_user.get_mis_datos(), \
                           is_authenticated=current_user.is_authenticated, \
                           rol='Gerencia')