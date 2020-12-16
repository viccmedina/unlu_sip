from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_stock.forms import AgregarStock,ConsultarStock, ExportarStock
from distribuidora.models.stock import TipoMovimientoStock
from distribuidora.models.producto import Producto,Marca, UnidadMedida
from distribuidora.core.gestion_stock.constants import TITULO, ROL
from distribuidora.core.gestion_stock.helper import *
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora import db
from flask_weasyprint import HTML, render_pdf, CSS
import json

stock = Blueprint('stock', __name__, template_folder='templates', static_folder='static')

@stock.route('/stock', methods=['GET'])
@login_required
def index():
    if current_user.has_role('Operador'):
        return render_template('home_stock.html', \
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador', \
        site='Gestión de Stock',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

    abort(403)

@stock.route('/stock/consultar', methods=['POST', 'GET'])
@login_required
def consultar_stock():
	if current_user.has_role('Operador'):
		id_producto = None
		id_marca = None
		id_um = None
		products = None
		form = ConsultarStock()
		form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
		form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
		form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
		if form.validate_on_submit():
			id_producto = form.producto.data
			id_marca = form.marca.data
			id_um = form.uMedida.data

			products = consulta_sotck(id_producto,id_marca,id_um)
			# hacer algo con los error de devolucine de id
			print("Productooo: {} ".format(products))
			if products == -777 :
				flash("el producto ingresado es incorrecto", 'error')
				products = None
			else:
				if products == -888 :
					flash('La unidad de medida ingresada es incorrecta', 'error')
					products = None
				else:
					if products == -999 :
						flash("La marca ingresada es incorrecta", 'error')
						products = None
					else:
						if products == -666:
							flash("El nombre de producto ingresado es incorrecto", 'error')
							products = None
						else:
							if products == -555:
								flash("No se han encontrados registros para los valores ingresados", 'warning')
								products = None

								print(form.errors, flush=True)

		return render_template('form_consultar_stock.html', \
		datos=current_user.get_mis_datos(),\
		is_authenticated=current_user.is_authenticated, \
		rol='operador', \
		products=products, \
		form=form, \
		site=TITULO,\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

	abort(403)


@stock.route('/stock/agregar', methods=['POST', 'GET'])
@login_required
def agregar():
	if current_user.has_role('Operador'):
		resultado = None
		id_producto = None
		id_marca = None
		id_um = None
		form = AgregarStock()
		#form.tipo_movimiento.choices = [(descripcion.descripcion) for descripcion in TipoMovimientoStock.query.all()]
		form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
		form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
		form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
		if form.validate_on_submit():
			tipo_mov = form.tipo_movimiento.data
			id_producto = form.producto.data
			id_marca = form.marca.data
			id_um = form.uMedida.data
			cantidad = form.cantidad.data
			try:
				cantidad = int(cantidad)
				if (cantidad >= 0) and (cantidad <= 1000000):
					# obtenemos el producto envase id
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
								# debo verificar que el producto envase id tenga stock real suficiente
								p = ProductoEnvase.query.filter_by(producto_id=product).first()
								print('00000000000000000000000000000000000000000000000')
								print('stock real : {}'.format(p.get_stock_real()))

								user =current_user.get_id()
								if current_user.has_role('Operador'):
									if tipo_mov == 'entrada':
										resultado = agregar_stock(user, product, cantidad, id_producto)
										print(resultado, flush=True)
										print('#'*80, flush=True)
										flash("El producto se ha cargado correctamente", 'warning')
									else:
										if p.get_stock_real() < cantidad:
											flash('La cantidad a descontar no es suficiente', 'error')
										else:
											resultado = salida(user, product, cantidad, id_producto)
											print(resultado, flush=True)
											print('#'*80, flush=True)
											flash("Se ha descontado el stock con exito", 'warning')
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
		form=form,\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

	abort(403)

@stock.route('/stock/exportar', methods=['POST', 'GET'])
@login_required
def exportar():
	if current_user.has_role('Operador'):
		resultado = None
		fecha_hasta = None
		fecha_desde = None
		form = ExportarStock()

		if form.validate_on_submit():
			fecha_desde = form.fecha_desde.data
			fecha_hasta = form.fecha_hasta.data
			if fecha_hasta is None:
				fecha_hasta = datetime.datetime.now()

			if fecha_hasta < fecha_desde:
				flash("ERROR, la FECHA HASTA es menor a FECHA DESDE",'error')
			else:
				resultado = consultaMovimientosExportar(fecha_desde,fecha_hasta)
				#print("lengt {}".format(resultado.length))
				print('#'*80, flush=True)
				#nro_cta = get_nro_cuenta_corriente(cliente)
				#resultado = get_consulta_movimientos(fecha_desde, fecha_hasta,nro_cta[0]['cuenta_corriente_id'])
				#print(resultado, flush=True)
				print('#'*80, flush=True)
		else:
			print(form.errors, flush=True)

		return render_template('exportar_movimientos.html', \
			datos=current_user.get_mis_datos(), \
			is_authenticated=current_user.is_authenticated, \
			resultado=resultado, \
			fecha_desde=fecha_desde,\
			fecha_hasta=fecha_hasta,\
			form=form, \
			site=TITULO,\
			rol='operador',\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)



@stock.route('/stock/importar', methods=['GET'])
@login_required
def importar():
	if current_user.has_role('Operador'):
		return render_template('importar_movimientos.html', \
		datos=current_user.get_mis_datos(), \
		is_authenticated=current_user.is_authenticated, \
		rol='operador',\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)


@stock.route('/stock/descargar/consulta')
@login_required
def descargar_consulta_stock():
	if current_user.has_role('Operador'):
		resultado = request.args.get("resultado", None)
		desde = request.args.get('fecha_desde')
		hasta = request.args.get('fecha_hasta')
		print('RESULTADOO!')
		print(resultado)
		print('desde: {}'.format(desde))
		print('hasta: {}'.format(hasta))
		movimientos = get_movimientos_by_fechas(desde, hasta)
		print('MOVIMIENTOS -------- {}'.format(movimientos))

		html = render_template('tabla_consulta_stock_css.html',\
			desde=desde,\
			hasta=hasta,\
			resultado=movimientos)
		"""
		stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
		return render_pdf(HTML(string=html), stylesheets=stylesheets)
		"""

		return render_pdf(HTML(string=html))
	abort(403)
