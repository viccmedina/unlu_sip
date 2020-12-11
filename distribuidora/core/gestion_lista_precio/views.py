from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_lista_precio.forms import *
from distribuidora.core.gestion_lista_precio.helper import *
from distribuidora.models.producto import *

from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora import db

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
        form = ConsultarProducto()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            products = consulta_precio_pProductoMarcaUMedida(id_producto,id_marca,id_um)


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
        form = AgregarProducto()
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


@lista_precio.route('/modificar', methods=['GET','POST'])
@login_required
def modificar():
    if current_user.has_role('Operador'):
        return render_template('form_modificar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        rol='operador')
    abort(403)


@lista_precio.route('/eliminar', methods=['GET','POST'])
@login_required
def eliminar():
    if current_user.has_role('Operador'):
        return render_template('form_eliminar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/exportar', methods=['GET','POST'])
@login_required
def exportar():
    if current_user.has_role('Operador'):
    	return render_template('exportar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/lista_precio/importar', methods=['GET','POST'])
@login_required
def importar():
    if current_user.has_role('Operador'):
        form = ImportarListaPrecio()
        return render_template('importar_lista_precio.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol='operador',\
        site='Importar Lista de Precios',\
        form=form)
    abort(403)
