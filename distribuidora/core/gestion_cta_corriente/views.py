from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.models.cuenta_corriente import MovimientoCtaCorriente
from distribuidora import db
from distribuidora.core.gestion_cta_corriente.query import CONSULTA_CTA_CORRIENTE


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
    """
    Nos permite consultar los movimientos de las ctas corrientes
    de los clientes. Para esto debemos preguntar que parámetros
    recibimos.
    Los parámetros válidos son:
    - Tipo Movimiento
    - Fecha Desde
    - Fecha Hasta
    """

    # Por ahora esto será hardcodeado.
    fecha_desde = None
    fecha_hasta = None
    tipo_movimiento = 'Deuda'
    resp = None
    status = None
    msg = None
    if fecha_hasta is not None and fecha_desde is not None \
        and tipo_movimiento is not None: 
        status = 'ERROR'
        msg = 'Todos los parametros son nulos! Al menos uno debe ser ingresado.'
    else:
        if fecha_desde is not None:
            status = 'ERROR_FECHA'
            msg = 'Las fechas son Nulas!. Al menos la fecha_desde debe ser ingresada'
        else:
            result = db.engine.execute(CONSULTA_CTA_CORRIENTE.format(fecha_desde = '2020-10-25 18:00:00', fecha_hasta = '2020-10-25 22:00:00'))
            mov = {}
            for row in result:
                
                mov[row['movimiento_id']] = {
                    "tipo_movimiento": row['tipo_movimiento_cta_corriente'],
                    "saldo": row['saldo'],
                    "fecha": row['ts_created']
                }

            resp = mov
            msg = 'Datos encontrados!'
            status = 'OK'

    respuesta = {
        "status": status,
        "msg": msg,
        "respuesta": resp
    }
    return respuesta

