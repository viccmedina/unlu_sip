from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_informes.forms import *
from distribuidora.core.gestion_informes.helper import *
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora import db
from flask_weasyprint import HTML, render_pdf, CSS
import json


informe = Blueprint('informe', __name__, template_folder='templates', static_folder='static')

@informe.route('/informe', methods=['GET'])
@login_required
def index():
    if current_user.has_role('Operador'):

        return render_template('home_informes.html', \
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador', \
        site='Gestión de Informes',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

    abort(403)


@informe.route('/informe/cta_corriente', methods=['POST', 'GET'])
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
                resultado = get_consulta_movimientos(fecha_desde,fecha_hasta)

        return render_template('gestionar_informe_cta_corriente.html', \
            datos=current_user.get_mis_datos(),	\
            is_authenticated=current_user.is_authenticated, rol='Operador', form=form, \
            resultado=resultado, site= 'Gestión de Informes - Consulta',\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)


@informe.route('/informe/devoluciones', methods=['POST', 'GET'])
@login_required
def consultar_devoluciones():
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
                    resultado = get_consulta_devoluciones(fecha_desde,fecha_hasta)

        return render_template('gestionar_informe_devoluciones.html', \
        datos=current_user.get_mis_datos(),	\
        is_authenticated=current_user.is_authenticated, rol='Operador', form=form, \
        resultado=resultado, site= 'Gestión de Informes - Consulta',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)



@informe.route('/informe/stock', methods=['POST', 'GET'])
@login_required
def consultar_stock():
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
                print("Acaaaa")
                resultado = get_consulta_stock(fecha_desde,fecha_hasta)
                print("pasoo")

        return render_template('gestionar_informe_stock.html', \
        datos=current_user.get_mis_datos(),	\
        is_authenticated=current_user.is_authenticated, rol='Operador', form=form, \
        resultado=resultado, site= 'Gestión de Informes - Consulta',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)


@informe.route('/informe/lista_precios', methods=['POST', 'GET'])
@login_required
def consultar_listado_precios():
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
                    resultado = get_consulta_lista_precios(fecha_desde,fecha_hasta)

        return render_template('gestionar_informe_lista_precios.html', \
        datos=current_user.get_mis_datos(),	\
        is_authenticated=current_user.is_authenticated, rol='Operador', form=form, \
        resultado=resultado, site= 'Gestión de Informes - Consulta',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)




@informe.route('/informe/productos', methods=['POST', 'GET'])
@login_required
def consultar_productos():
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
                    resultado = get_consulta_productos(fecha_desde,fecha_hasta)

        return render_template('gestionar_informe_productos.html', \
        datos=current_user.get_mis_datos(),	\
        is_authenticated=current_user.is_authenticated, rol='Operador', form=form, \
        resultado=resultado, site= 'Gestión de Informes - Consulta',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)



@informe.route('/informe/descargar/consulta')
@login_required
def descargar_consulta():
    if current_user.has_role('Operador'):
        resultado = request.args.get('resultado')
        print(resultado, flush=True)
        resultado = json.loads(resultado.replace("'", '"'))
        html = render_template('tabla_cuentas_corriente.html', resultado=resultado)
        return render_pdf(HTML(string=html))
    abort(403)
