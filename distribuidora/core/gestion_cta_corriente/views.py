from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.models.cuenta_corriente import MovimientoCtaCorriente
from distribuidora import db
from distribuidora.core.gestion_cta_corriente.forms import ConsultarMovimientos

import datetime

cta_corriente = Blueprint('cta_corriente', __name__, template_folder='templates')

@cta_corriente.route('/cta_corriente', methods=['GET'])
@login_required
def index():
	if current_user.has_role('Operador'):
		return render_template('home_cta_corriente.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol='operador', \
            site='Gestión Ctas Corrientes')

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

@cta_corriente.route('/consultar/movimientos', methods=['GET'])
def consultar_movimientos():

	form = ConsultarMovimientos()
	if form.validate_on_submit():
		fecha_desde = form.fecha_desde.data
		fecha_hasta = form.fecha_hasta.data
		if fecha_hasta is None:
			fecha_hasta = datetime.datetime.now()

		cliente = form.cliente.data
