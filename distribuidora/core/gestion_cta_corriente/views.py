from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db

cta_corriente = Blueprint('cta_corriente', __name__, template_folder='templates')

@cta_corriente.route('/cta_corriente', methods=['GET'])
@login_required
def index():
	if current_user.has_role('Operador'):
		return render_template('home_cta_corriente.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol='operador')

@cta_corriente.route('/consultar', methods=['GET'])
@login_required		
def consultar_cta_corriente():
    return render_template('form_consultar_cta_corriente.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@cta_corriente.route('/agregar', methods=['GET'])
@login_required	
def agregar():
	return render_template('form_agregar_movimiento.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@cta_corriente.route('/exportar', methods=['GET'])
@login_required	
def exportar():
	return render_template('exportar_movimientos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')

@cta_corriente.route('/importar', methods=['GET'])
@login_required	
def importar():
	return render_template('importar_movimientos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')