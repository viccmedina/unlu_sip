from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.core.gestion_cta_corriente.constants import TITULO, ROL
from distribuidora.core.gestion_cta_corriente.helper import *
from distribuidora.core.gestion_cta_corriente.forms import ConsultarMovimientos, \
	AgregarMovimiento, ConsultarSaldo
from distribuidora.models.cuenta_corriente import MovimientoCtaCorriente, TipoMovimientoCtaCorriente
from distribuidora.models.gestion_usuario import Usuario
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
		if nro_cta == -999 :
			flash("La cuenta ingresada es incorrecta", 'error')
		else:
			resultado = get_consulta_movimientos(fecha_desde, fecha_hasta, nro_cta)
	else:
		print(form.errors, flush=True)

	return render_template('form_consultar_cta_corriente.html', \
		datos=current_user.get_mis_datos(),	\
		is_authenticated=current_user.is_authenticated, rol=ROL, form=form, \
		resultado=resultado, site= TITULO + ' - Consulta')

@cta_corriente.route('/cta_corriente/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    form = AgregarMovimiento()
    form.tipo_movimiento.choices = [(descripcion.descripcion) for descripcion in TipoMovimientoCtaCorriente.query.all()]
    if form.validate_on_submit():
        tipo_movimiento = form.tipo_movimiento.data
        cliente = form.cliente.data
        monto = form.monto.data
        print('#'*80, flush=True)
        nro_cta = get_nro_cuenta_corriente(cliente)
        print(nro_cta, flush=True)
        #ni bien se inserta el pago, debo ir a verificar el el monto ingresado
        #mas el monto actual me alcanza para dar como pagado un pedido
        # para esto, me tengo que traer todos los comprobantes de pagos con estado
        #A (Adeuda), y ver el monto ahi, recorrer hasta encontrar uno para el que me
        #alcance.

        usuario_id = current_user.get_id()
        user = Usuario.query.filter_by(id=usuario_id).first()
        print('movimiento ---> {}'.format(tipo_movimiento), flush=True)
        new_mov_cta_corriente(nro_cta,tipo_movimiento,user.id,monto)
        saldo = obtener_saldo_cta_corriente(nro_cta)
        if tipo_movimiento == 'Pago':
            actualizar_estado_comprobante_pago(saldo, monto, cliente)
        flash("La transacción se ha registrado con éxito", 'success')
    else:
        print(form.errors, flush=True)
        flash("Algo salió mal, verifique los datos ingresados", 'error')

    return render_template('form_agregar_movimiento_cta_corriente.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol=ROL, \
    site=TITULO + ' - Nuevo Movimiento', \
    form=form)

@cta_corriente.route('/cta_corriente/consultarSaldo', methods=['GET', 'POST'])
@login_required
def consultar_saldo():
	resultado = None
	form = ConsultarSaldo()

	if form.validate_on_submit():
		cliente = form.cliente.data
		nro_cta = get_nro_cuenta_corriente(cliente)
		if nro_cta == -999 :
			flash("La cuenta ingresada es incorrecta", 'error')
		else:
			resultado = consulta_saldo(nro_cta)
	else:
		print(form.errors, flush=True)

	return render_template('consultar_saldo_cta_corriente.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
	resultado=resultado,\
	form=form,\
    rol=ROL, \
	site= TITULO + ' - Consultar Saldo')

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
def descargar_consulta_cta_corriente(resultado):
	resultado = json.loads(resultado.replace("'", '"'))
	html = render_template('tabla_movimientos_cta_corriente.html', resultado=resultado)
	return render_pdf(HTML(string=html))
