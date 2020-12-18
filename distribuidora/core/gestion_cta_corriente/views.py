from flask import render_template, url_for, flash, redirect, request,\
    Blueprint, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.core.gestion_cta_corriente.constants import TITULO, ROL
from distribuidora.core.gestion_cta_corriente.helper import *
from distribuidora.core.gestion_cta_corriente.forms import *
from distribuidora.models.cuenta_corriente import MovimientoCtaCorriente, TipoMovimientoCtaCorriente
from distribuidora.models.gestion_usuario import Usuario
from flask_weasyprint import HTML, render_pdf
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
import datetime
import json

cta_corriente = Blueprint('cta_corriente', __name__, template_folder='templates')

def cargar_errores(errores):
    """
    Pasamos el diccionario con todos los errores levantados por Flask
    """
    for key, value in errores.items():
        for v in value:
            flash(v, 'error')

@cta_corriente.route('/cta_corriente', methods=['GET'])
@login_required
def index():
    if current_user.has_role('Operador'):
        return render_template('home_cta_corriente.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol='operador',\
            site=TITULO,\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)

@cta_corriente.route('/cta_corriente/consultar', methods=['POST', 'GET'])
@login_required
def consultar_cta_corriente():
    if current_user.has_role('Operador'):
        resultado = None
        form = ConsultarMovimientos()
        if form.validate_on_submit():
            fecha_desde = form.fecha_desde.data
            fecha_hasta = form.fecha_hasta.data
            if fecha_hasta is None:
                fecha_hasta = datetime.datetime.now()
            if fecha_hasta < fecha_desde :
                flash("ERROR, la FECHA HASTA es menor que la FECHA DESDE",'error')
            else:
                cliente = form.cliente.data
                print('CLIENTE --> {}'.format(cliente))
                nro_cta = get_nro_cuenta_corriente(cliente)

                if nro_cta:
                    nro_cta = nro_cta[0]['cuenta_corriente_id']
                    resultado = get_consulta_movimientos(fecha_desde, fecha_hasta, nro_cta)
                else:
                    flash("La cuenta ingresada es incorrecta", 'error')

        return render_template('form_consultar_cta_corriente.html', \
            datos=current_user.get_mis_datos(),	\
            is_authenticated=current_user.is_authenticated, rol=ROL, form=form, \
            resultado=resultado, site= TITULO + ' - Consulta',\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)

@cta_corriente.route('/cta_corriente/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    if current_user.has_role('Operador'):
        form = AgregarMovimiento(request.form, meta={'locales': ['es_ES', 'es']})
        form.tipo_movimiento.choices = [\
            (descripcion.descripcion) for descripcion in TipoMovimientoCtaCorriente.query.all()\
            ]
        if form.validate_on_submit():
            tipo_movimiento = form.tipo_movimiento.data
            cliente = form.cliente.data
            monto = form.monto.data
            nro_cta = get_nro_cuenta_corriente(cliente)
            print(nro_cta, flush=True)
            if len(nro_cta) > 0:
                nro_cta = nro_cta[0]['cuenta_corriente_id']
                usuario_id = current_user.get_id()
                user = Usuario.query.filter_by(id=usuario_id).first()
                resultado = new_mov_cta_corriente(nro_cta, tipo_movimiento, user.id, monto)
                saldo = consulta_saldo(nro_cta)
                if tipo_movimiento == 'Pago':
                    if actualizar_estado_comprobante_pago(monto, cliente):
                        flash("Pago agregar correctamente", 'success')
                else:
                    flash("Algo salió mal, verifique los datos ingresados", 'error')

                if resultado:
                    flash("La transacción se ha registrado con éxito", 'success')
                else:
                    flash("Algo salió mal, verifique los datos ingresados", 'error')
            else:
                flash("La cuenta ingresada no existe.", 'error')
        else:
            cargar_errores(form.errors)

        return render_template('form_agregar_movimiento_cta_corriente.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol=ROL, \
        site=TITULO + ' - Nuevo Movimiento', \
        form=form,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)


@cta_corriente.route('/cta_corriente/consultarSaldo', methods=['GET', 'POST'])
@login_required
def consultar_saldo():
    if current_user.has_role('Operador'):
        resultado = None
        saldito = None
        form = ConsultarSaldo()

        if form.validate_on_submit():
            cliente = form.cliente.data
            nro_cta = get_nro_cuenta_corriente(cliente)

            if not nro_cta:
                flash("El cliente no posee una Cta Corriente", 'error')
            else:
                nro_cta = nro_cta[0]['cuenta_corriente_id']
                saldito = consulta_saldo_aparte(nro_cta)
                resultado = consulta_saldo(nro_cta)
        else:
            cargar_errores(form.errors)


        return render_template('consultar_saldo_cta_corriente.html', \
            datos=current_user.get_mis_datos(), \
            is_authenticated=current_user.is_authenticated, \
            resultado=resultado,\
            saldito=saldito,\
            form=form,\
            rol=ROL, \
            site= TITULO + ' - Consultar Saldo',\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)





@cta_corriente.route('/cta_corriente/exportar', methods=['POST', 'GET'])
@login_required
def exportar():
	if current_user.has_role('Operador'):
		resultado = None
		fecha_hasta = None
		fecha_desde = None
		form = ExportarCtaCorriente()

		if form.validate_on_submit():
			resultado = consultaCtaCorrienteExportar()
			#print("lengt {}".format(resultado.length))
			print('#'*80, flush=True)
			print('#'*80, flush=True)
		else:
			print(form.errors, flush=True)

		return render_template('exportar_movimientos_cta_corriente.html', \
			datos=current_user.get_mis_datos(), \
			is_authenticated=current_user.is_authenticated, \
			resultado=resultado, \
			form=form, \
			site=TITULO,\
			rol='operador',\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)





@cta_corriente.route('/cta_corriente/importar', methods=['GET'])
@login_required
def importar():
    if current_user.has_role('Operador'):
    	return render_template('importar_movimientos_cta_corriente.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol=ROL, \
    	site= TITULO + ' - Importar',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)


@cta_corriente.route('/cta_corriente/descargar/consulta')
@login_required
def descargar_consulta_cta_corriente():
    if current_user.has_role('Operador'):
        resultado = request.args.get("resultado", None)
        print('RESULTADOO!')
        print(resultado)
        result = consultaCtaCorrienteExportar()

        html = render_template('tabla_consulta_cta_corriente_css.html',resultado=result)
        """
        stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
        return render_pdf(HTML(string=html), stylesheets=stylesheets)
        """

        return render_pdf(HTML(string=html))
    abort(403)
