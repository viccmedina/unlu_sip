from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_stock.forms import agregarStock,consultarStock
from distribuidora.models.stock import TipoMovimientoStock
from distribuidora.core.gestion_stock.constants import TITULO, ROL
from distribuidora.core.gestion_stock.helper import get_id_producto, consulta_sotck, agregar_stock, deolucion
from distribuidora.models.gestion_usuario import Usuario
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
	id_producto = None
	id_marca = None
	id_um = None
	form = consultarStock()

	if form.validate_on_submit():

		id_producto = form.producto.data
		id_marca = form.marca.data
		id_um = form.uMedida.data
		print('#'*80, flush=True)
		product = get_id_producto(id_producto,id_marca,id_um)
		# hacer algo con los error de devolucine de id
		print("Productooo: {} ".format(product))
		if product == -777 :
			flash("el producto ingresado es incorrecto", 'error')
		else:
			if product == -888 :
				flash('La unidad de medida ingresada es incorrecta', 'error')
			else:
				if product == -999 :
					flash("La marca ingresada es incorrecta", 'error')
				else:
					resultado = consulta_sotck(product)
					print(resultado, flush=True)
					print('#'*80, flush=True)
	else:
		print(form.errors, flush=True)

	return render_template('form_consultar_stock.html', \
		datos=current_user.get_mis_datos(),\
		is_authenticated=current_user.is_authenticated, \
		rol='operador', \
		producto=id_producto, \
		marca=id_marca, \
		uMedida=id_um, \
		resultado=resultado, \
		form=form, \
		site=TITULO)




@stock.route('/agregar', methods=['POST', 'GET'])
@login_required
def agregar():
	resultado = None
	id_producto = None
	id_marca = None
	id_um = None
	form = agregarStock()
	form.tipo_movimiento.choices = [(descripcion.descripcion) for descripcion in TipoMovimientoStock.query.all()]
	if form.validate_on_submit():
		tipo_mov = form.tipo_movimiento.data
		id_producto = form.producto.data
		id_marca = form.marca.data
		id_um = form.uMedida.data
		cantidad = form.cantidad.data
		try:
			cantidad = int(cantidad)
			if (cantidad >= 0) and (cantidad <= 1000000):
				product = get_id_producto(id_producto,id_marca,id_um)
				if product == -777 :
					flash("el producto ingresado es incorrecto", 'error')
				else:
					if product == -888 :
						flash('La unidad de medida ingresada es incorrecta', 'error')
					else:
						if product == -999 :
							flash("La marca ingresada es incorrecta", 'error')
						else:
							user = Usuario.query.filter_by(username='operador').first()
							if user.has_role('Operador'):
								if tipo_mov == 'entrada':
									resultado = agregar_stock(user.id,product,cantidad,id_producto)
									print(resultado, flush=True)
									print('#'*80, flush=True)
									flash("El producto se ha cargado correctamente", 'warning')
								else:
									resultado = deolucion(user.id,product,cantidad,id_producto)
									print(resultado, flush=True)
									print('#'*80, flush=True)
									flash("Devolucion registrada con exito", 'warning')
							else:
								flash("Usuario incorrecto, contacte al administrador", 'error')
			else:
				flash("La cantidad ingresada es incorrecta", 'error')
		except ValueError as e:
			flash("La cantidad ingresada es incorrecta", 'error')
	else:
		print(form.errors, flush=True)

	return render_template('form_agregar_movimiento.html', \
	datos=current_user.get_mis_datos(), \
	is_authenticated=current_user.is_authenticated, \
	rol='operador',\
	producto=id_producto, \
	marca=id_marca, \
	uMedida=id_um, \
	resultado=resultado, \
	site=TITULO ,\
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
