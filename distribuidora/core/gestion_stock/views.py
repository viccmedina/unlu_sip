from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
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

@stock.route('/consultar', methods=['GET'])
@login_required		
def consultar_stock():
    return render_template('form_consultar_stock.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@stock.route('/agregar', methods=['GET'])
@login_required	
def agregar():
	return render_template('form_agregar_movimiento.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


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