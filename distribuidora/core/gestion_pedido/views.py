from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.models.pedido import PedidoEstado, Pedido, DetallePedido
from distribuidora.core.gestion_pedido.helper import *
from distribuidora.core.gestion_pedido.forms import NuevoPedido, FormAgregarProducto

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
        else:
            flash('ERROOOOOR, ya existe un pedido en curso', 'error')
            print('ERROOOOOR, ya existe un pedido en curso', flush=True)
    return render_template('form_nuevo_pedido.html', datos=current_user.get_mis_datos(), is_authenticated=current_user.is_authenticated, rol=current_user.get_role(), form=form, site='Gestión de Pedido')

@pedido.route('/pedido/consultar', methods=['GET'])
@login_required
def consultar_pedido():
	return render_template('form_consultar_pedido.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol=current_user.get_role(), \
            site='Gestión de Pedido')

@pedido.route('/pedido/anular', methods=['GET'])
def anular_pedido():
	pass

@pedido.route('/pedido/modificar', methods=['GET'])
def modificar_pedido():
	pass

@pedido.route('/pedido/confirmar/cliente', methods=['GET'])
def confirmar_pedido_cliente():
	"""
	necesito id del pedido
	verificar que el estado del pedido sea: Pendiente Confirmación Cliente
	luego pasarlo a:  Pendiente Confirmación Operador
	"""
	pass

@pedido.route('/pedido/confirmar/operador', methods=['GET'])
def confirmar_pedido_operador():
	"""
	necesito verificar que el estado del pedido sea :  Pendiente Confirmación Operador
	"""

	pass
