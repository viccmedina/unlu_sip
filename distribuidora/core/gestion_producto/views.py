from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_producto.forms import ImportarProducto
from distribuidora.core.gestion_pedido.forms import FormAgregarProducto
from distribuidora.core.gestion_pedido.helper import get_cantidad_estados_pedido, \
    get_ultimo_pedido_id, insert_into_detalle_pedido
from distribuidora.core.gestion_producto.helper import *

from distribuidora.models.producto import Producto, Marca, ProductoEnvase, Envase, TipoProducto

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

@producto.route('/producto/listar', methods=['GET', 'POST'])
@login_required
def listar_productos():
    page = request.args.get('page', 1, type=int)
    productos = db.session.query(Producto, Marca, TipoProducto).filter(\
        Producto.marca_id == Marca.marca_id).filter(\
        Producto.tipo_producto_id == TipoProducto.tipo_producto_id).paginate( page, 5, False)

    print('-'*88, flush=True)
    print(productos.items, flush=True)
    print('-'*88, flush=True)

    return render_template('listar_productos.html', \
    datos=current_user.get_mis_datos(), \
    is_authenticated=current_user.is_authenticated, \
    rol='operador', \
    site='Listado de Productos', \
    producto=productos)

@producto.route('/producto/detalle', methods=['GET', 'POST'])
@login_required
def detalle_producto():
    producto = request.args.get('producto', type=str)
    marca = request.args.get('marca', type=str)
    if producto is not None and marca is not None:
        print('producto {}'.format(producto), flush=True)
        print('marca {}'.format(marca), flush=True)
        print('#'*88, flush=True)
        producto_id = get_producto_by_descripcion_marca(producto, marca)
    else:
        producto_envase_id = request.args.get('producto', type=int)
        producto_id = get_producto_id_from_producto_envase(producto_envase_id)
    print('productoooooooos {}'.format(producto_id), flush=True)
    productos = get_producto_envase_by_producto_id(producto_id[0]['producto_id'])
    print('#'*88, flush=True)
    print(productos, flush=True)
    print('#'*88, flush=True)
    form = FormAgregarProducto()
    if form.validate_on_submit():
        #obtengo los datos del cliente
        usuario_id = current_user.get_id()
        print('^'*50, flush=True)
        print(usuario_id, flush=True)
        print('^'*50, flush=True)
        #recupero el pedido en estado pcc
        pedido_id = get_ultimo_pedido_id(usuario_id)
        #recupero la cantidad de estados de ese pedido
        cantidad_estados = get_cantidad_estados_pedido(pedido_id)
        if cantidad_estados == 1:
            producto_id = request.args.get("producto")
            cantidad = form.cantidad.data
            print('.'*88, flush=True)
            print('cantidad: {}'.format(cantidad), flush=True)
            print('producto: {}'.format(producto_id), flush=True)
            print('.'*88, flush=True)
            insert_into_detalle_pedido(pedido_id=pedido_id, producto_envase_id=producto_envase_id, cantidad=cantidad)
    else:
        print(form.errors)

    return render_template('detalle_producto.html', form=form, productos=productos)
