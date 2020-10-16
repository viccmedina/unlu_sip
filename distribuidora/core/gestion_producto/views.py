from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db

producto = Blueprint('producto', __name__, template_folder='templates')

@producto.route('/producto', methods=['GET'])
@login_required
def index():
	if current_user.has_role('Operador'):
		return render_template('home_producto.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol='operador')

@producto.route('/consultar', methods=['GET'])
@login_required		
def consultar_producto():
    return render_template('form_consultar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/agregar', methods=['GET'])
@login_required	
def agregar():
	return render_template('form_agregar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/modificar', methods=['GET'])
@login_required 
def modificar():
    return render_template('form_modificar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/eliminar', methods=['GET'])
@login_required 
def eliminar():
    return render_template('form_eliminar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/exportar', methods=['GET'])
@login_required	
def exportar():
	return render_template('exportar_productos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')

@producto.route('/importar', methods=['GET'])
@login_required	
def importar():
	return render_template('importar_productos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')