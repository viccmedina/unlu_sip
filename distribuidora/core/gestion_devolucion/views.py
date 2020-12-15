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

		return render_template('devolucion.html',\
			is_authenticated=current_user.is_authenticated,\
			datos=current_user.get_mis_datos(),\
			site='Gestión Devoluciones',\
			rol=current_user.get_role(),\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)

@devolucion.route('/devolucion/pedidos/listar', methods=['POST','GET'])
@login_required
def listar_pedidos_para_devolucion():
	if current_user.has_role('Cliente') or current_user.has_role('Operador') :
		usuario_id = current_user.get_id()
		pedidos_id = buscar_pedido_id(usuario_id)
		return render_template('pedidos_para_devolucion.html',\
			is_authenticated=current_user.is_authenticated,\
			datos=current_user.get_mis_datos(),\
			site='Gestión Devoluciones',\
			rol=current_user.get_role(),\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
			pedidos_id=pedidos_id)
	abort(403)

@devolucion.route('/devolucion/listar', methods=['POST','GET'])
@login_required
def listar_devoluciones():
	if current_user.has_role('Cliente') or current_user.has_role('Operador') :
		usuario_id = current_user.get_id()
		pedidos_id = buscar_pedido_id(usuario_id)
		devoluciones = get_all_devoluciones(usuario_id)
		print('PEDIDOS ----- {}'.format(pedidos_id))
		print('DEVOLUCIONES ------ {}'.format(devoluciones))

		return render_template('devoluciones_generadas.html',\
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
		form = NuevaDevolucion()
		form.motivo.choices = [(descripcion.descripcion) for descripcion in MotivoDevolucion.query.all()]
		print('MOTIVOSSSSSSS {}'.format(form.motivo.choices))
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
		pedido_id = request.args.get('pedido')
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

		return redirect(url_for('devoluciones.listar_pedidos_para_devolucion'))
	abort(403)

@devolucion.route('/devolucion/cliente/confirmacion', methods=['POST','GET'])
@login_required
def confirmar_devolucion_cliente():
	if current_user.has_role('Cliente'):
		print('confirmacion de devolucion por parte del cliente')
		devolucion_id = request.args.get('detalle')
		result = check_producto_devolucion(devolucion_id)
		print("devolucion_id ----- : {}".format(devolucion_id))
		print("devolucion_id ----- : {}".format(result))
		if len(result) > 0:
			print(result)
			devolucion_id = result[0]['devolucion_id']
			update = update_estado_devolucion(devolucion_id, 'CPC')
			if update:
				# mandar a guardar esto en el historial de devolucion
				insert_into_historial_devolucion(devolucion_id, 'CPC')
				flash('Devolución enviada para ser procesada', 'success')
			else:
				flash('Algo salió mal, comuniquese con el operador', 'error')
		else:
			flash('Para confirmar la devolución tiene que tener al menos un producto', 'error')

		return redirect(url_for('devoluciones.index'))
	abort(403)

@devolucion.route('/devolucion/operador/listar', methods=['POST','GET'])
@login_required
def listar_devoluciones_operador():
	if current_user.has_role('Operador'):
		form = ActualizarEstadoDevolucion()
		form.estado.choices = ['RECHAZADA', 'ACEPTADA', 'CONCRETADA']
		devoluciones = get_all_devoluciones_operador()
		if not devoluciones:
			devoluciones = None
		return render_template('devoluciones_vista_operador.html',\
			devoluciones=devoluciones,\
			form=form,\
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated,\
			site='Gestion Devoluciones',\
			rol=current_user.get_role(),\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)

@devolucion.route('/devolucion/operador/listar/detalle', methods=['POST','GET'])
@login_required
def listar_detalle_devoluciones_operador():
	if current_user.has_role('Operador'):
		devolucion_id = request.args.get('devolucion')
		print('DEVOLUCION ID: ---- {}'.format(devolucion_id))
		detalle_devolucion = get_detalle_devolucion(devolucion_id)
		print('DETALLE DEVOLUCION')
		print(detalle_devolucion)
		return render_template('devoluciones_vista_operador_detalle.html',\
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated,\
			site='Gestion Devoluciones',\
			rol=current_user.get_role(),\
			devolucion=detalle_devolucion,\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)
	
@devolucion.route('/devolucion/operador/confirmacion', methods=['POST','GET'])
@login_required
def actualizar_estado_devolcion_operador():
	if current_user.has_role('Operador'):
		form = ActualizarEstadoDevolucion()
		estado = form.estado.data
		print('ESTADO!!!')
		print(estado)
		if form.validate_on_submit():
			estado_nuevo = form.estado.data
			estado_anterior = request.args.get('estado_anterior')
			devolucion = request.args.get('devolucion')
			estado = get_devolucion_estado_by_descripcion(estado_nuevo)
			# necesito pasar el id de la devolución + descripcion corta del nuevo estado
			update = update_estado_devolucion(devolucion, estado[0]['descripcion_corta'])
			print('UPDATE!!!!!: {}'.format(update))
			# si pudo actualizar en tbl devolucion, agregamos al historial
			if update:
				insert_into_historial_devolucion(devolucion, estado[0]['descripcion_corta'])
				flash('Estado actualizado', 'success')
				body = 'La devolución #{} : fue - {}'.format(devolucion, estado_nuevo)
				receptor = get_devolucion_pedido(devolucion)
				print('RECEPTOR --- {}'.format(receptor))
				data = {
					"body": body,
					"emisor": current_user.get_id(),
					"receptor": receptor[0]['usuario_id']
				}
				resp = insert_nuevo_mensaje(data)

				if resp:
					flash('Mensaje enviado', 'success')
				else:
					flash('Algo salió mal, verifique los datos', 'warning')
			else:
				flash('No es posible actualizar el estado', 'error')
		else:
			flash('Ocurrió un erro en la carga de datos.', 'error')
	
		return redirect(url_for('devoluciones.listar_devoluciones_operador'))
	abort(403)