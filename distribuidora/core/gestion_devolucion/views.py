from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify,abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer, insert_nuevo_mensaje
from distribuidora import db
from distribuidora.core.gestion_devolucion.forms import *
from distribuidora.core.gestion_devolucion.helper import *
from distribuidora.models.producto import *
from distribuidora.models.devolucion import EstadoDevolucion
from distribuidora.core.gestion_devolucion.helper import *
from distribuidora.core.gestion_pedido.helper import get_detalle_pedido

devolucion = Blueprint('devoluciones', __name__, template_folder='templates')

@devolucion.route('/devolucion/index', methods=['POST','GET'])
@login_required
def index():
	if current_user.has_role('Cliente') or current_user.has_role('Operador') :
		usuario_id = current_user.get_id()
		pedidos_id = buscar_pedido_id(usuario_id)
		devoluciones = get_all_devoluciones(usuario_id)
		print('PEDIDOS ----- {}'.format(pedidos_id))
		print('DEVOLUCIONES ------ {}'.format(devoluciones))


		return render_template('devolucion.html',\
		datos=current_user.get_mis_datos(),\
		site='Gestión Devoluciones',\
		rol=current_user.get_role(),\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
		pedidos_id=pedidos_id, \
		devoluciones=devoluciones)
	abort(403)



@devolucion.route('/devolucion/detallePedido', methods=['POST','GET'])
@login_required
def ver_detalle():
	if current_user.has_role('Cliente'):
		pedidos_id = request.args.get('pedido')
		print(pedidos_id)
		#det_pedido = detalle_pedidos(pedidos_id)
		det_pedido = get_detalle_pedido(pedidos_id)
		print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
		print(det_pedido)
		form = NuevaDevolucion()
		form.motivo.choices = [(descripcion.descripcion) for descripcion in EstadoDevolucion.query.all()]

		return render_template('detalle_pedido_devolucion.html',form=form,\
		datos=current_user.get_mis_datos(),\
		site='Gestion Devoluciones',\
		rol=current_user.get_role(),\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
		det_pedido=det_pedido)
	abort(403)



@devolucion.route('/devolucion/nueva', methods=['POST','GET'])
@login_required
def nueva_devolucion():
	if current_user.has_role('Cliente'):
		print("Volviooo aca")
		
		pedido_id = request.args.get('pedido')
		print("pedido ----- : {}".format(pedido_id))
		# Necesito generar una nueva devolucion
		result = generar_nueva_devolucion(pedido_id)
		if result:
			flash('La solicitud de una devolución ha sido generada, por favor agregue los productos asociados', 'success')
		else:
			flash('Algo salió mal', 'error')

		return redirect(url_for('devoluciones.index'))
	abort(403)
