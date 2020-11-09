from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_stock.forms import agregarStock,consultarStock
from distribuidora.models.producto import Producto
from distribuidora.core.gestion_stock.constants import TITULO, ROL
from distribuidora.core.gestion_stock.helper import get_id_producto, consulta_sotck
from distribuidora import db

stock = Blueprint('stock', __name__, template_folder='templates')

@stock.route('/stock', methods=['GET'])
@login_required
def index():
	if current_user.has_role('Operador'):
		return render_template('home_stock.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol='operador', \
            site='Gestión de Stock')


@stock.route('/consultar', methods=['POST', 'GET'])
@login_required
def consultar_stock():
	resultado = None
	form = consultarStock()
	if form.validate_on_submit():
		#hacer la consulta por el id del product
		p = form.producto.data
		m = form.marca.data
		um = form.uMedida.data
		#formProducto = p +" marca "+ m + um
		print('#'*80, flush=True)
		product = get_id_producto(p,m,um)
		print("Productooo: {} ".format(product) )
		resultado = consulta_sotck(product[0]['producto_id'])
		print(resultado, flush=True)
		print('#'*80, flush=True)
	else:
		print(form.errors, flush=True)
	return render_template('form_consultar_stock.html', \
		datos=current_user.get_mis_datos(),\
		is_authenticated=current_user.is_authenticated, \
		rol='operador', \
		producto=p, \
		marca=m, \
		uMedida=um, \
		resultado=resultado, \
		form=form, \
		site=TITULO)




@stock.route('/agregar', methods=['GET'])
@login_required
def agregar():
    form = agregarStock()
    form.choice_producto.choices = [(producto.id, producto.descripcion)
                                    for producto in Producto.query.all()]
    return render_template('form_agregar_movimiento.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador',\
    site='Agregar stock',\
    form=form)

@stock.route('/exportar', methods=['GET'])
@login_required
def exportar():
	return render_template('exportar_movimientos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')

@stock.route('/importar', methods=['GET'])
@login_required
def importar():

	return render_template('importar_movimientos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')
