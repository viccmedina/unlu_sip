from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_lista_precio.forms import ImportarListaPrecio
from distribuidora import db

lista_precio = Blueprint('lista_precio', __name__, template_folder='templates')

@lista_precio.route('/lista_precio', methods=['GET'])
@login_required
def index():
    if current_user.has_role('Operador'):
        return render_template('home_lista_precio.html', \
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador', \
        site='Gestión de Precios')
    abort(403)

@lista_precio.route('/consultar', methods=['GET'])
@login_required		
def consultar_lista_precio():
    if current_user.has_role('Operador'):
        return render_template('form_consultar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/agregar', methods=['GET'])
@login_required	
def agregar():
    if current_user.has_role('Operador'):
    	return render_template('form_agregar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/modificar', methods=['GET'])
@login_required 
def modificar():
    if current_user.has_role('Operador'):
        return render_template('form_modificar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/eliminar', methods=['GET'])
@login_required 
def eliminar():
    if current_user.has_role('Operador'):
        return render_template('form_eliminar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/exportar', methods=['GET'])
@login_required	
def exportar():
    if current_user.has_role('Operador'):
    	return render_template('exportar_lista_precio.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)


@lista_precio.route('/lista_precio/importar', methods=['GET'])
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