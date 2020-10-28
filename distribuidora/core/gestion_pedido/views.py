from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.models.pedido import TipoPedido, EstadoPedido, Pedido, DetallePedido

pedido = Blueprint('pedido', __name__, template_folder='templates')

@pedido.route('/pedido', methods=['GET'])
@login_required
def index():
	return render_template('home_pedido.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol=current_user.get_role(), \
            site='Gestión de Pedido')

@pedido.route('/pedido/nuevo', methods=['GET'])
@login_required
def nuevo_pedido():
	return render_template('form_nuevo_pedido.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol=current_user.get_role(), \
            site='Gestión de Pedido')

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
	pass

@pedido.route('/pedido/confirmar/operador', methods=['GET'])
def confirmar_pedido_operador():
	nro_pedido = 1
	pass
