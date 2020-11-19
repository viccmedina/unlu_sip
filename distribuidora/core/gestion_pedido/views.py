from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.models.pedido import PedidoEstado, Pedido, DetallePedido
from distribuidora.core.gestion_pedido.helper import *
from distribuidora.core.gestion_pedido.forms import NuevoPedido, FormAgregarProducto, \
    ModificarDetallePedido, ActualizarEstadoPedido

pedido = Blueprint('pedido', __name__, template_folder='templates')

@pedido.route('/pedido', methods=['GET'])
@login_required
def index():
	return render_template('home_pedido.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol=current_user.get_role(), \
            site='Gestión de Pedido')

@pedido.route('/pedido/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pedido():
    form = NuevoPedido()
    if form.validate_on_submit():
        #recuperamos el id del usuario
        usuario_id = current_user.get_id()
        pedido_id = get_ultimo_pedido_id(usuario_id)
        #recupero la cantidad de estados de ese pedido
        cantidad_estados = get_cantidad_estados_pedido(pedido_id)
        if cantidad_estados > 1 or pedido_id is None:
            estado = 'PCC'
            estado_id = get_estado_pedido_id(estado)
            crear_nuevo_pedido(usuario_id, estado_id[0]['pedido_estado_id'])
            flash('Pedido Creadooooo!', 'success')
        else:
            flash('ERROOOOOR, ya existe un pedido en curso', 'error')
    return render_template('form_nuevo_pedido.html',\
         datos=current_user.get_mis_datos(),\
         is_authenticated=current_user.is_authenticated,\
         rol=current_user.get_role(),\
         form=form, site='Gestión de Pedido')

@pedido.route('/pedido/consultar', methods=['GET'])
@login_required
def consultar_pedido():
    pedido_pcc = get_listado_pedidos_pcc(usuario_id=current_user.get_id())
    if not pedido_pcc:
        pedido_pcc = None
    page = request.args.get('page', 1, type=int)
    pedidos_todos = db.session.query(Pedido).filter(\
        Pedido.usuario_id==current_user.get_id(), Pedido.estado_pedido_id!=1).paginate( page, 5, False)
    print(pedidos_todos.items, flush=True)
    return render_template('form_consultar_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido',\
        pedido_pcc=pedido_pcc,
        pedidos_todos=pedidos_todos)

@pedido.route('/pedido/anular', methods=['GET', 'POST'])
def anular_pedido():
    form = ModificarDetallePedido()
    pedido_id = request.args.get('pedido_id', None)
    result = anular_pedido_por_cliente(pedido_id)
    if result:
        flash('Pedido anulado correctamente', 'success')
    else:
        flash('Ocurrió un error', 'error')
    pedido_pcc = get_listado_pedidos_pcc(usuario_id=current_user.get_id())
    if not pedido_pcc:
        pedido_pcc = None
    return render_template('form_consultar_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido',\
        pedido_pcc=pedido_pcc)

@pedido.route('/pedido/detalle/modificar', methods=['GET', 'POST'])
def modificar_detalle_producto():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    if form.validate_on_submit():
        detalle = request.args.get('detalle_pedido', type=int)
        producto = request.args.get('producto', type=int)
        cantidad = form.cantidad.data
        result = update_detalle_producto(pedido, detalle, cantidad)
        if result:
            flash('Actualizado Correctamente !', 'success')
        else:
            flash('Algo Salió mal :( !', 'error')
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html', detalle=detalle, form=form)

@pedido.route('/pedido/detalle/eliminar', methods=['GET'])
def eliminar_producto_detalle():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    producto_envase_id = request.args.get('producto_envase_id', type=int)
    detalle_id = request.args.get('detalle_pedido', type=int)
    result = eliminar_producto_detalle_pedido(producto_envase_id, detalle_id, pedido)
    if result:
        flash('Producto Eliminado Correctamente !', 'success')
    else:
        flash('Algo Salió mal :( !', 'error')
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html', detalle=detalle, form=form)

@pedido.route('/pedido/confirmar/cliente', methods=['GET', 'POST'])
def confirmar_pedido_cliente():
    pedido_pcc = request.args.get('pedido_pcc', type=int)
    if pedido_pcc is not None:
        if actualizar_estado_pedido(pedido_pcc, 'PCO'):
            flash('Pedido confirmado correctamente', 'success')
        else:
            flash('Ocurrió un Error!', 'error')
    return redirect(url_for('pedido.consultar_pedido'))


@pedido.route('/pedido/modificar/estado/operador', methods=['GET', 'POST'])
def modificar_estado_operador():
    form = ActualizarEstadoPedido()
    pedido = request.args.get('pedido', type=int)
    if form.validate_on_submit():
        #nuevo estado, el que queremos insertar
        estado_nuevo = form.estado.data
        print('^'*90, flush=True)
        print('estado nuevo {}'.format(estado_nuevo), flush=True)
        #estado actual del pedido
        estado_actual = request.args.get('estado_anterior', type=str)
        print('estado_actual {}'.format(estado_actual), flush=True)
        print('^'*90, flush=True)
        result = actualizar_pedido_estado_por_operador(current_user.get_id(),\
            pedido, estado_nuevo, estado_actual)
        if result:
            flash('ESTADO ACTUALIZADOOO !', 'success')
        else:
            flash('ALGO SALIO MAL :(', 'error')
        print('^'*90, flush=True)

    pedidos = get_listado_pedidos_pco()
    return render_template('listado_pedidos.html', pedidos=pedidos, form=form)

@pedido.route('/pedido/listar/operador', methods=['GET'])
def listar_pedido_operador():
    pedidos = None
    form = ActualizarEstadoPedido()
    if current_user.has_role('Operador'):
        pedidos = get_listado_pedidos_pco()
    return render_template('listado_pedidos.html', pedidos=pedidos, form=form)

@pedido.route('/pedido/listar/detalle', methods=['GET'])
def listar_detalle_pedido():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html', detalle=detalle, form=form)

@pedido.route('/pedido/repetir', methods=['GET', 'POST'])
def repetir_pedido():
    pedido = request.args.get('pedido')
    print('¬'*70, flush=True)
    print(pedido, flush=True)
    print('¬'*70, flush=True)
    nuevo_pedido_desde_pedido_anterior(current_user.get_id(), pedido)
    return None
