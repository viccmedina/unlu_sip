from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer, insert_nuevo_mensaje
from distribuidora import db
from distribuidora.core.gestion_devolucion.forms import *
from distribuidora.core.gestion_devolucion.helper import *
from distribuidora.models.producto import *
from distribuidora.models.devolucion import EstadoDevolucion
from distribuidora.core.gestion_pedido.helper import get_detalle_pedido

devolucion = Blueprint('devoluciones', __name__, template_folder='templates')

@devolucion.route('/devolucion/index', methods=['POST','GET'])
@login_required
def index():
	if current_user.has_role('Cliente'):
		usuario_id = current_user.get_id()
		pedidos_id = buscar_pedido_id(usuario_id)
		for row in pedidos_id:
			print("pedido {}".format(row))


		form = NuevaDevolucion()


		#if form.validate_on_submit():
			#producto = form.producto.data
			#marca = form.marca.data
			#umedida = form.uMedida.data


		return render_template('devolucion.html',form=form,\
		datos=current_user.get_mis_datos(),\
		site='Gestion Devoluciones',\
		rol=current_user.get_role(),\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
		pedidos_id=pedidos_id)
	abort(403)



@devolucion.route('/devolucion/detallePedido', methods=['POST','GET'])
@login_required
def ver_detalle():
	if current_user.has_role('Cliente'):
		pedidos_id = request.args.get('p')
		#det_pedido = detalle_pedidos(pedidos_id)
		det_pedido = get_detalle_pedido(pedidos_id)
		form = NuevaDevolucion()
		form.motivo.choices = [(descripcion.descripcion) for descripcion in EstadoDevolucion.query.all()]

		return render_template('detalle_pedido_devolucion.html',form=form,\
		datos=current_user.get_mis_datos(),\
		site='Gestion Devoluciones',\
		rol=current_user.get_role(),\
		sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
		det_pedido=det_pedido)
	abort(403)



@devolucion.route('/devolucion/devoluciones', methods=['POST','GET'])
@login_required
def devolver():
	if current_user.has_role('Cliente'):
		print("Volviooo aca")
		form = NuevaDevolucion()
		pedidos_id = request.args.get('arr')
		#for row in pedido_id:
			#print("row tiene: {}".format(pedidos_id))

		return redirect(url_for('devoluciones.index'))
	abort(403)
