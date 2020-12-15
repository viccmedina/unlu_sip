from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_informes.forms import *
from distribuidora.core.gestion_informes.helper import *
from distribuidora.models.gestion_usuario import Usuario
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora import db
from distribuidora.models.precio import Lista_precio
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
                resultado = get_consulta_movimientos()

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
        form = FormStock()
        if form.validate_on_submit():
            resultado = get_consulta_stock()

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
        form = ConsultarPrecios()
        form.id_precio.choices = [(precio_id.precio_id) for precio_id in Lista_precio.query.all()]
        if form.validate_on_submit():
            #resultado = get_consulta_lista_precios(fecha_desde,fecha_hasta)
            id = form.id_precio.data
            print("id  antes de url for{}".format(id))
            fechas = constultar_id_precio(id)
            for row in fechas:
                return redirect(url_for('informe.consultar_listado_precio',ini=row.ini,fin=row.fin,id=id))

        return render_template('gestionar_informe_lista_precios.html', \
        datos=current_user.get_mis_datos(),	\
        is_authenticated=current_user.is_authenticated, rol='Operador', form=form, \
        resultado=resultado,  site= 'Gestión de Informes - Consulta',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)




@informe.route('/informe/productos', methods=['POST', 'GET'])
@login_required
def consultar_productos():
    if current_user.has_role('Operador'):
        resultado = None
        form = FormProducto()
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





@informe.route('/informe/lista_precio', methods=['POST', 'GET'])
@login_required
def consultar_listado_precio():
    if current_user.has_role('Operador'):
        resultado = None
        ini = request.args.get('ini')
        fin = request.args.get('fin')
        id = request.args.get('id')


        form1 = ConsultarPrecios2()
        form1.fecha_desde.data= ini
        form1.fecha_hasta.data = fin
        if form1.validate_on_submit():
            id = request.args.get('id')

            resultado = get_consulta_lista_precios(id=id)
            print("resutado {}".format(resultado))

            return render_template('gestionar_informe_lista_precio.html', \
            datos=current_user.get_mis_datos(),	\
            is_authenticated=current_user.is_authenticated, rol='Operador', form1=form1, \
            resultado=resultado,id=id, site= 'Gestión de Informes - Consulta',\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),ini=ini,fin=fin)

        return render_template('gestionar_informe_lista_precio.html', \
        datos=current_user.get_mis_datos(),	\
        is_authenticated=current_user.is_authenticated, rol='Operador', form1=form1, \
        resultado=resultado, id=id,site= 'Gestión de Informes - Consulta',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),ini=ini,fin=fin)
    abort(403)


@informe.route('/informe/cta_corriente/descargar/consulta')
@login_required
def descargar_consulta_cta_corriente():
    if current_user.has_role('Operador'):
        movimientos = get_consulta_movimientos()
        html = render_template('tabla_consulta_cta_corriente_css.html',resultado=movimientos)
        """
        stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
        return render_pdf(HTML(string=html), stylesheets=stylesheets)
        """

        return render_pdf(HTML(string=html))
    abort(403)



@informe.route('/informe/stock/descargar/consulta')
@login_required
def descargar_consulta_stock():
    if current_user.has_role('Operador'):
        movimientos = get_consulta_stock()

        html = render_template('tabla_consultar_stock_css.html',resultado=movimientos)
        """
        stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
        return render_pdf(HTML(string=html), stylesheets=stylesheets)
        """

        return render_pdf(HTML(string=html))
    abort(403)


@informe.route('/informe/lista_precios/descargar/consulta')
@login_required
def descargar_consulta_lista_precios():
    if current_user.has_role('Operador'):
        id = request.args.get('id')
        print(" agarro id antes consulta {}".format(id))
        resultado = get_consulta_lista_precios(id=id)
        for row in resultado:
            print("resultado {}".format(row))

        html = render_template('tabla_consultar_lista_precios_css.html',resultado=resultado)
        """
        stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
        return render_pdf(HTML(string=html), stylesheets=stylesheets)
        """

        return render_pdf(HTML(string=html))
    abort(403)


@informe.route('/informe/productos/descargar/consulta')
@login_required
def descargar_consulta_producto():
    if current_user.has_role('Operador'):
        desde = request.args.get('desde')
        hasta = request.args.get('hasta')
        print("hasta {}".format(hasta))
        print("desde {}".format(desde))
        resultado = get_consulta_productos(desde,hasta)
        for row in resultado:
            print("resultado {}".format(row))

        html = render_template('tabla_consultar_productos_css.html',resultado=resultado,desde=desde,hasta=hasta)
        """
        stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
        return render_pdf(HTML(string=html), stylesheets=stylesheets)
        """

        return render_pdf(HTML(string=html))
    abort(403)
