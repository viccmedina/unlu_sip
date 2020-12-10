from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_stock.forms import AgregarStock,ConsultarStock, ExportarStock
from distribuidora.models.stock import TipoMovimientoStock
from distribuidora.models.producto import Producto,Marca, UnidadMedida
from distribuidora.core.gestion_stock.constants import TITULO, ROL
from distribuidora.core.gestion_stock.helper import get_id_producto, \
	consulta_sotck, agregar_stock, salida, consultaMovimientosExportar
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora import db
from flask_weasyprint import HTML, render_pdf, CSS
import json


informe = Blueprint('informe', __name__, template_folder='templates', static_folder='static')

@informe.route('/informe', methods=['GET'])
@login_required
def index():
    if current_user.has_role('Operador'):

        return render_template('home_informes.html', \
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador', \
        site='Gestión de Informes',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

    abort(403)
