from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_producto.forms import ImportarProducto
from distribuidora.core.gestion_producto.helper import get_lista_productos
from distribuidora import db

producto = Blueprint('producto', __name__, template_folder='templates')

@producto.route('/producto', methods=['GET'])
@login_required
def index():
	if current_user.has_role('Operador'):
		return render_template('home_producto.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol='operador', \
            site='Gestión de Productos')

@producto.route('/consultar', methods=['GET'])
@login_required		
def consultar_producto():
    return render_template('form_consultar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/agregar', methods=['GET'])
@login_required	
def agregar():
	return render_template('form_agregar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/modificar', methods=['GET'])
@login_required 
def modificar():
    return render_template('form_modificar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/eliminar', methods=['GET'])
@login_required 
def eliminar():
    return render_template('form_eliminar_producto.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')


@producto.route('/exportar', methods=['GET'])
@login_required	
def exportar():
	return render_template('exportar_productos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador')

@producto.route('/producto/importar', methods=['GET'])
@login_required	
def importar():
    form=ImportarProducto()
    return render_template('importar_producto.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador', \
        site='Importar Producto', \
        form=form)

@producto.route('/producto/listar', methods=['GET'])
@login_required 
def listar_productos():
    productos = get_lista_productos()
    print(productos, flush=True)
    return render_template('listar_productos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador', \
    site='Listado de Productos', \
    productos=productos)