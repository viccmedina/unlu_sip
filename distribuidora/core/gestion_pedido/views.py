from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.models.pedido import PedidoEstado, Pedido, DetallePedido
from distribuidora.core.gestion_pedido.helper import *
from distribuidora.core.gestion_pedido.forms import NuevoPedido, FormAgregarProducto, \
    ModificarDetallePedido

pedido = Blueprint('pedido', __name__, template_folder='templates')

@pedido.route('/pedido', methods=['GET'])
@login_required
def index():
	return render_template('home_pedido.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol=current_user.get_role(), \
            site='Gestión de Pedido')

@pedido.route('/pedido/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pedido():
    form = NuevoPedido()
    if form.validate_on_submit():
        #recuperamos el id del usuario
        usuario_id = current_user.get_id()
        pedido_id = get_ultimo_pedido_id(usuario_id)
        #recupero la cantidad de estados de ese pedido
        cantidad_estados = get_cantidad_estados_pedido(pedido_id)
        if cantidad_estados > 1:
            estado = 'PCC'
            estado_id = get_estado_pedido_id(estado)
            print(estado_id, flush=True)
            print(estado_id[0]['pedido_estado_id'], flush=True)
            crear_nuevo_pedido(usuario_id, estado_id[0]['pedido_estado_id'])
            flash('Pedido Creadooooo!', 'success')
        else:
            flash('ERROOOOOR, ya existe un pedido en curso', 'error')
            print('ERROOOOOR, ya existe un pedido en curso', flush=True)
    return render_template('form_nuevo_pedido.html', datos=current_user.get_mis_datos(), is_authenticated=current_user.is_authenticated, rol=current_user.get_role(), form=form, site='Gestión de Pedido')

@pedido.route('/pedido/consultar', methods=['GET'])
@login_required
def consultar_pedido():
    print(current_user.get_id(), flush=True)
    pedido_pcc = get_listado_pedidos_pcc(usuario_id=current_user.get_id())
    if not pedido_pcc:
        pedido_pcc = None
    print('-'*90, flush=True)
    print(pedido_pcc, flush=True)
    return render_template('form_consultar_pedido.html', datos=current_user.get_mis_datos(), is_authenticated=current_user.is_authenticated, rol=current_user.get_role(), site='Gestión de Pedido', pedido_pcc=pedido_pcc)

@pedido.route('/pedido/anular', methods=['GET'])
def anular_pedido():
	pass

@pedido.route('/pedido/detalle/modificar', methods=['GET', 'POST'])
def modificar_detalle_producto():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    print('pedido: {}'.format(pedido), flush=True)
    if form.validate_on_submit():
        detalle = request.args.get('detalle_pedido', type=int)
        producto = request.args.get('producto', type=int)
        cantidad = form.cantidad.data
        print('cantidad: {}'.format(cantidad), flush=True)
        print('producto: {}'.format(producto), flush=True)
        print('detalle_pedido: {}'.format(detalle), flush=True)
        result = update_detalle_producto(pedido, detalle, cantidad)
        if result:
            flash('Actualizado Correctamente !', 'success')
        else:
            flash('Algo Salió mal :( !', 'error')
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html', detalle=detalle, form=form)

@pedido.route('/pedido/detalle/eliminar', methods=['GET'])
def eliminar_producto_detalle():
	pass

@pedido.route('/pedido/confirmar/cliente', methods=['GET', 'POST'])
def confirmar_pedido_cliente():
    pedido_pcc = request.args.get('pedido_pcc', type=int)
    print('*'*90)
    print(pedido_pcc, flush=True)
    if pedido_pcc is not None:
        print('PEDIDO PASADO X PARAMETRO QUE VAMOS A CONFIRMAR', flush=True)
        print(pedido_pcc, flush=True)
        actualizar_estado_pedido(pedido_pcc, 'PCO')
        print('PEDIDO CONFIRMADO POR CLIENTE', flush=True)
    return redirect(url_for('pedido.consultar_pedido'))


@pedido.route('/pedido/confirmar/operador', methods=['GET'])
def confirmar_pedido_operador():
	"""
	necesito verificar que el estado del pedido sea :  Pendiente Confirmación Operador
	"""

	pass

@pedido.route('/pedido/listar/operador', methods=['GET'])
def listar_pedido_operador():
    pedidos = None
    if current_user.has_role('Operador'):
        pedidos = get_listado_pedidos_pco()
    return render_template('listado_pedidos.html', pedidos=pedidos)

@pedido.route('/pedido/listar/detalle', methods=['GET'])
def listar_detalle_pedido():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    print('pedido {}'.format(pedido), flush=True)
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html', detalle=detalle, form=form)
