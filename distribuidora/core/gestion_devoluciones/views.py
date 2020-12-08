from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_devoluciones.forms import *
from distribuidora.core.gestion_devoluciones.helper import *
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora.models.devolucion import *
from distribuidora.models.producto import Producto, Marca, ProductoEnvase, Envase, TipoProducto, \
UnidadMedida, TipoProducto

from distribuidora import db

devolucion = Blueprint('devolucion', __name__, template_folder='templates')


@devolucion.route('/devolucion', methods=['POST','GET'])
@login_required
def index():
    if current_user.has_role('Cliente'):
        form = NuevaDevolucion()

        return render_template('realizar_devolucion.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol='cliente',\
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        site='Gestión de Devoluciones',\
        form=form)
    abort(403)

@devolucion.route('/devolucion/agregar', methods=['POST','GET'])
@login_required
def devolucion():
    if current_user.has_role('Cliente'):
        form = NuevaDevolucion()

        return render_template('realizar_devolucion.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol='cliente',\
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        site='Gestión de Devoluciones',\
        form=form)
    abort(403)
