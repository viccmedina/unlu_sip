from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from distribuidora.core.gestion_lista_precio.forms import *
from distribuidora.core.gestion_lista_precio.helper import *
from distribuidora.models.producto import *
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora import db, app
from distribuidora.models.producto import Producto
from datetime import datetime
import os

lista_precio = Blueprint('lista_precio', __name__, template_folder='templates')

@lista_precio.route('/lista_precio', methods=['GET','POST'])
@login_required
def index():
    if current_user.has_role('Operador'):


        return render_template('home_lista_precio.html', \
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated, \
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        rol='operador', \
        site='Gestión de Precios')
    abort(403)


@lista_precio.route('/consultar/precio', methods=['GET','POST'])
@login_required
def consultar_lista_precio():
    if current_user.has_role('Operador'):
        products = None
        form = ConsultarPrecio()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            products = consulta_precio_pProductoMarcaUMedida(id_producto,id_marca,id_um)
            if products == None:
                flash("Producto invalido", 'error')

        return render_template('form_consultar_lista_precios.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,rol='operador',\
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        form=form,\
        products=products,\
        site='Gestion de Precios')
    abort(403)


@lista_precio.route('/agregar/precio', methods=['GET','POST'])
@login_required
def agregar():
    if current_user.has_role('Operador'):
        products = None
        form = AgregarPrecios()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            precio = form.cantidad.data
            fecha = form.fecha_vigencia.data
            agregar_precio_pProductoMarcaUMedida(id_producto,id_marca,id_um,precio,fecha)
            flash("Precio agregado con exito",'warning')

        return render_template('form_agregar_lista_precios.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        rol='operador',\
        form=form,\
        site='Gestion de Precios')
    abort(403)


@lista_precio.route('/modificar/precios', methods=['GET','POST'])
@login_required
def modificar():
    if current_user.has_role('Operador'):
        id_producto = None
        id_marca = None
        id_um = None
        b = None
        products = None
        form = ModificarPrecios()

        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            products = consulta_precio_pProductoMarcaUMedida(id_producto,id_marca,id_um)


            if products == None:
                #flash("Se ha Eliminado el producto", 'warning')
                flash("No se ha podido localizar el producto, producto invalido",'error')
            else:
                return redirect(url_for('lista_precio.modificar_precios',producto=form.producto.data,marca=form.marca.data,umed=form.uMedida.data))


        return render_template('form_modificar_lista_precios.html', \
        datos=current_user.get_mis_datos(), \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador'  ,\
        form=form,\
        products=products)
    abort(403)



@lista_precio.route('/lista_precio/exportar', methods=['POST', 'GET'])
@login_required
def exportar():
	if current_user.has_role('Operador'):
		resultado = None
		fecha_hasta = None
		fecha_desde = None
		form = ExportarListaPrecio()

		if form.validate_on_submit():
			resultado = consultaListaPreciosExportar()
			print('#'*80, flush=True)
		else:
			print(form.errors, flush=True)

		return render_template('exportar_lista_precio.html', \
			datos=current_user.get_mis_datos(), \
			is_authenticated=current_user.is_authenticated, \
			resultado=resultado, \
			form=form, \
			site='Gestión de Lista Precios',\
			rol='operador',\
			sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
	abort(403)




@lista_precio.route('/lista_precio/importar', methods=['GET','POST'])
@login_required
def importar_lista_precio():
    if current_user.has_role('Operador'):


        if 'file' not in request.files:
            pass
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            extension = filename.split('.')
            if extension[1] not in app.config['UPLOAD_EXTENSIONS']:
                flash('La extensión del archivo no es la correcta. Se aceptan: {}'.format(app.config['UPLOAD_EXTENSIONS']), 'error')
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path = app.config['UPLOAD_FOLDER'] + filename
                result = importar_lista_precios_from_file(path)
                flash(result, 'warning')



        form = ImportarListaPrecio()
        return render_template('importar_lista_precio.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol='operador',\
        site='Importar Lista de Precios',\
        form=form,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)


@lista_precio.route('/lista_precio/modificar', methods=['POST','GET'])
@login_required
def modificar_precios():
    if current_user.has_role('Operador'):
        vigencia = "2020-01-01 00:00:00"
        pro = request.args.get('producto')
        mar = request.args.get('marca')
        um = request.args.get('umed')
        form1 = ModifiPrecios()

        product = consulta_precio_pProductoMarcaUMedida(pro,mar,um)

        products = consultar_precio_pProductoMarcaUMedida(pro,mar,um)
        for row in products:
            print("Precio {}".format(row.precio))
            p = str(row.precio)
            f = row.vigencia
            producto = row.id
            hoy = str(row.hoy)
        print("Hoy {}".format(hoy))
        if form1.validate_on_submit():

            precio = str(form1.cantidad.data)
            print("precio1 {}".format(precio))
            print("precio2 {}".format(p))
            fech = str(form1.fecha_vigencia.data)
            print("fechaaaaaa {}".format(p))
            if str(precio) == str(p):
                print("Las fech son distintas")

            if str(precio) == str(p) and (fech == vigencia):
                flash("No has realizado ningun cambio",'warning')
                return redirect(url_for('lista_precio.modificar'))
            else:
                if str(precio) == str(p) and (fech != vigencia):
                    if fech < hoy:
                        flash("Error, la fecha ingresada no puede ser menor a 'HOY'",'error')
                        return redirect(url_for('lista_precio.modificar'))
                    else:
                        modificarFecha(fech,producto,f)
                        flash("La fecha se ha cambiado con exito",'warning')
                        return redirect(url_for('lista_precio.modificar'))
                else:
                    if str(precio) != str(p) and (fech == vigencia):
                        modificarPrecio(precio,producto)
                        flash("El precio se ha modificado con exito",'warning')
                        return redirect(url_for('lista_precio.modificar'))
                    else:
                        modificarPrecioFecha(fech,precio,producto,f)
                        flash("El precio y la fecha se han modificado con exito",'warning')
                        return redirect(url_for('lista_precio.modificar'))

        return render_template('form_modificar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador'  ,\
        form1=form1,\
        products=product,\
        precio=p,\
        fecha=f)

    abort(403)

@lista_precio.route('/lista_precio/descargar/consulta')
@login_required
def descargar_consulta_lista_precio():
	if current_user.has_role('Operador'):
		resultado = request.args.get("resultado", None)
		print('RESULTADOO!')
		print(resultado)
		result = consultaListaPreciosExportar()

		html = render_template('tabla_consulta_lista_precio_css.html',\
			resultado=result)
		"""
		stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"]
		return render_pdf(HTML(string=html), stylesheets=stylesheets)
		"""

		return render_pdf(HTML(string=html))
	abort(403)