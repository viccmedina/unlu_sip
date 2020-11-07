from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.core.gestion_cta_corriente.constants import TITULO, ROL
from distribuidora.core.gestion_cta_corriente.helper import get_consulta_movimientos, \
	get_nro_cuenta_corriente
from distribuidora.core.gestion_cta_corriente.forms import ConsultarMovimientos, \
	AgregarMovimiento
from distribuidora.models.cuenta_corriente import MovimientoCtaCorriente
from flask_weasyprint import HTML, render_pdf
import datetime
import json

cta_corriente = Blueprint('cta_corriente', __name__, template_folder='templates')


@cta_corriente.route('/cta_corriente', methods=['GET'])
@login_required
def index():
	if current_user.has_role('Operador'):
		return render_template('home_cta_corriente.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol='operador', \
            site=TITULO)

@cta_corriente.route('/cta_corriente/consultar', methods=['POST', 'GET'])
@login_required
def consultar_cta_corriente():

	resultado = None
	form = ConsultarMovimientos()
	if form.validate_on_submit():
		fecha_desde = form.fecha_desde.data
		fecha_hasta = form.fecha_hasta.data
		if fecha_hasta is None:
			fecha_hasta = datetime.datetime.now()

		cliente = form.cliente.data
		print('#'*80, flush=True)
		nro_cta = get_nro_cuenta_corriente(cliente)
		resultado = get_consulta_movimientos(fecha_desde, fecha_hasta, \
			nro_cta[0]['cuenta_corriente_id'])
		print(resultado, flush=True)
		print('#'*80, flush=True)
	else:
		print(form.errors, flush=True)

	return render_template('form_consultar_cta_corriente.html', \
		datos=current_user.get_mis_datos(),	\
		is_authenticated=current_user.is_authenticated, rol=ROL, form=form, resultado=resultado, site= TITULO + ' - Consulta')

@cta_corriente.route('/cta_corriente/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
	form = AgregarMovimiento()
	tipo_movimiento = form.tipo_movimiento.data
	monto = form.monto.data
	cliente = form.cliente.data
	print(monto, flush=True)
	print(tipo_movimiento, flush=True)
	print(cliente, flush=True)
	"""
	if form.validate_on_submit():
		tipo_movimiento = form.tipo_deuda.data
		monto = form.monto.data
		cliente = form.cliente.data
		print('#'*80, flush=True)
		nro_cta = get_nro_cuenta_corriente(cliente)
		print(resultado, flush=True)
		print('#'*80, flush=True)
	else:
		print(form.errors, flush=True)
	"""
	return render_template('form_agregar_movimiento_cta_corriente.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol=ROL, \
	site=TITULO + ' - Nuevo Movimiento', \
	form=form)


@cta_corriente.route('/cta_corriente/exportar', methods=['GET'])
@login_required
def exportar():
	return render_template('exportar_movimientos_cta_corriente.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol=ROL, \
	site= TITULO + ' - Exportar')

@cta_corriente.route('/cta_corriente/importar', methods=['GET'])
@login_required
def importar():
	return render_template('importar_movimientos_cta_corriente.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol=ROL, \
	site= TITULO + ' - Importar')


@cta_corriente.route('/cta_corriente/descargar/consulta/<string:resultado>.pdf')
@login_required
def descargar_consulta(resultado):
	resultado = json.loads(resultado.replace("'", '"'))
	html = render_template('tabla_movimientos_cta_corriente.html', resultado=resultado)
	return render_pdf(HTML(string=html))
