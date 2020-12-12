from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify,abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer, insert_nuevo_mensaje
from distribuidora import db
from distribuidora.core.gestion_devolucion.forms import *
from distribuidora.core.gestion_devolucion.helper import *
from distribuidora.models.producto import *
from distribuidora.models.devolucion import EstadoDevolucion, MotivoDevolucion
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
			is_authenticated=current_user.is_authenticated,\
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
		pedido_id = request.args.get('pedido')
		print(pedido_id)
				
		form = NuevaDevolucion()
		form.motivo.choices = [(descripcion.descripcion) for descripcion in MotivoDevolucion.query.all()]
		print('MOTIVOSSSSSSS {}'.format(form.motivo.choices))
		print('WWWWWWWWWWWWWWWWWWWWWWWWWWWW')
		cantidad = request.args.get('cantidad', None)
		print('Cantidad --- {}'.format(cantidad))
		detalle_pedido = request.args.get('detalle_pedido', None)
		print('detalle pedido ------ {}'.format(detalle_pedido))
		if form.validate_on_submit():
			print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
			print(form.motivo.data)
			motivo = form.motivo.data
			devolucion_id = get_devolucion_by_pedido(pedido_id)
			print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV')
			print(devolucion_id)
			devolucion_id = devolucion_id[0]['devolucion_id']
			# aca tenemos que validar que el producto que haya ingresado no exista en la devolucion
			result = check_producto_devolucion(detalle_pedido)
			print('lllllllllllllllllllllllllllllll')
			print(result)
			if not result:
				if agregar_producto_a_devolucion(motivo, cantidad, devolucion_id, detalle_pedido):
					flash('Producto agregado al reclamo', 'success')
				
			else:
				flash('Este reclamo ya se encuentra en el sistema', 'error')
				
		else:
			print(form.errors)

		det_pedido = get_detalle_pedido(pedido_id)
		print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
		print(det_pedido)
		return render_template('detalle_pedido_devolucion.html',form=form,\
		datos=current_user.get_mis_datos(),\
		is_authenticated=current_user.is_authenticated,\
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
		# Necesito verificar que el pedido no tenga una devolucion ya solicitada
		if get_devolucion_by_pedido(pedido_id):
			flash('Ya se generó una Devolución para este Pedido', 'warning')
		else:
			# Necesito generar una nueva devolucion
			result = generar_nueva_devolucion(pedido_id)
			if result:
				# mandar a guardar esto en el historial de devolucion
				devolucion_id = get_devolucion_by_pedido(pedido_id)
				devolucion_id = devolucion_id[0]['devolucion_id']
				insert_into_historial_devolucion(devolucion_id, 'ECC')
				flash('La solicitud de una devolución ha sido generada, por favor agregue los productos asociados', 'success')
			else:
				flash('Algo salió mal', 'error')

		return redirect(url_for('devoluciones.index'))
	abort(403)

@devolucion.route('/devolucion/cliente/confirmacion', methods=['POST','GET'])
@login_required
def confirmar_devolucion_cliente():
	print('confirmacion de devolucion por parte del cliente')
	devolucion_id = request.args.get('detalle')
	result = check_producto_devolucion(devolucion_id)
	print("devolucion_id ----- : {}".format(devolucion_id))
	print("devolucion_id ----- : {}".format(result))
	devolucion_id = result[0]['devolucion_id']
	update = update_estado_devolucion(devolucion_id, 'CPC')
	if update:
		# mandar a guardar esto en el historial de devolucion
		insert_into_historial_devolucion(devolucion_id, 'CPC')
		flash('Devolución enviada para ser procesada', 'success')
	else:
		flash('Algo salió mal, comuniquese con el operador', 'error')

	return redirect(url_for('devoluciones.index'))

@devolucion.route('/devolucion/operador/listar', methods=['POST','GET'])
@login_required
def listar_devoluicones_operador():
	pass


@devolucion.route('/devolucion/operador/confirmacion', methods=['POST','GET'])
@login_required
def actualizar_estado_devolcion_operador():
	pass

