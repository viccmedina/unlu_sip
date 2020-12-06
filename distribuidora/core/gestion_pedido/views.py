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
        if validar_nuevo_pedido(usuario_id):
            estado = 'PCC'
            estado_id = get_estado_pedido_id(estado)
            crear_nuevo_pedido(usuario_id, estado_id[0]['pedido_estado_id'])
            flash('Pedido creado satisfactoriamente!', 'success')
        else:
            flash('ERROR, ya existe un pedido en curso', 'error')
    return render_template('form_nuevo_pedido.html',\
         datos=current_user.get_mis_datos(),\
         is_authenticated=current_user.is_authenticated,\
         rol=current_user.get_role(),\
         form=form, site='Gestión de Pedido')

@pedido.route('/pedido/consultar', methods=['GET'])
@login_required
def consultar_pedido():
    if current_user.has_role('Cliente'):
        pedido_pcc = get_listado_pedidos_pcc(usuario_id=current_user.get_id())
        if not pedido_pcc:
            pedido_pcc = None
        page = request.args.get('page', 1, type=int)
        pedidos_todos = db.session.query(Pedido).filter(\
            Pedido.usuario_id==current_user.get_id(), Pedido.estado_pedido_id!=1).paginate( page, 5, False)
        return render_template('form_consultar_pedido.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol=current_user.get_role(),\
            site='Gestión de Pedido',\
            pedido_pcc=pedido_pcc,
            pedidos_todos=pedidos_todos)
    abort(403)

@pedido.route('/pedido/anular', methods=['GET', 'POST'])
@login_required
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
@login_required
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
            flash('Algo Salió mal !', 'error')
    else:
        flash('Algo Salió mal !', 'error')
    detalle = get_detalle_pedido(pedido)
    print('detalle_pedido ---> {}'.format(detalle), flush=True)
    return render_template('detalle_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido', \
        detalle=detalle,\
        form=form)

@pedido.route('/pedido/detalle/eliminar', methods=['GET'])
@login_required
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
    return render_template('detalle_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido', \
        detalle=detalle,\
        form=form)

@pedido.route('/pedido/confirmar/cliente', methods=['GET', 'POST'])
@login_required
def confirmar_pedido_cliente():
    if current_user.has_role('Cliente'):
        pedido_pcc = request.args.get('pedido_pcc', type=int)
        if pedido_pcc is not None:
            if actualizar_estado_pedido(pedido_pcc, 'PCO'):
                flash('Pedido confirmado correctamente', 'success')
            else:
                flash('Ocurrió un Error!', 'error')
        return redirect(url_for('pedido.consultar_pedido'))
    abort(403)


@pedido.route('/pedido/modificar/estado/operador', methods=['GET', 'POST'])
@login_required
def modificar_estado_operador():
    if current_user.has_role('Operador'):
        form = ActualizarEstadoPedido()
        pedido = request.args.get('pedido', type=int)
        if form.validate_on_submit():
            #nuevo estado, el que queremos insertar
            estado_nuevo = form.estado.data
            #estado actual del pedido
            estado_actual = request.args.get('estado_anterior', type=str)
            costo = None
            if estado_nuevo == 'EN PREPARACION':
                costo = actualizar_stock_real(pedido)
            
            result = actualizar_pedido_estado_por_operador(current_user.get_id(),\
                pedido, estado_nuevo, estado_actual, costo)

            if result:
                flash('Estado de pedido actualizado !', 'success')
            else:
                flash('ERROR! El nuevo estado no es posible :(', 'error')

        pedidos = get_listado_pedidos_pco()
        return render_template('listado_pedidos.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol=current_user.get_role(),\
            site='Gestión de Pedido',\
            pedidos=pedidos, form=form)
    abort(403)

@pedido.route('/pedido/listar/operador', methods=['GET'])
@login_required
def listar_pedido_operador():
    if current_user.has_role('Operador'):
        pedidos = None
        form = ActualizarEstadoPedido()
        if current_user.has_role('Operador'):
            pedidos = get_listado_pedidos_pco()
        return render_template('listado_pedidos.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol=current_user.get_role(),\
            site='Gestión de Pedido', \
            pedidos=pedidos, form=form)
    abort(403)


@pedido.route('/pedido/listar/detalle', methods=['GET'])
@login_required
def listar_detalle_pedido():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido', \
        detalle=detalle, \
        form=form)


@pedido.route('/pedido/listar/detalle/anterior', methods=['GET'])
@login_required
def listar_detalle_pedido_anterior():
    pedido = request.args.get('pedido', type=int)
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedidos_anteriores.html', detalle=detalle)

@pedido.route('/pedido/repetir', methods=['GET', 'POST'])
@login_required
def repetir_pedido():
    if current_user.has_role('Cliente'):
        usuario_id = current_user.get_id()
        if validar_nuevo_pedido(usuario_id):
            pedido = request.args.get('pedido')
            nuevo_pedido_desde_pedido_anterior(usuario_id, pedido)
            form = ModificarDetallePedido()
            detalle = get_detalle_pedido(pedido)
            flash('Pedido creado satisfactoriamente', 'success')
            return render_template('detalle_pedido.html', detalle=detalle, form=form)
        else:
            flash('ERROR! Ya existe un pedido en curso', 'error')
            return redirect(url_for('pedido.consultar_pedido'))
    abort(403)
