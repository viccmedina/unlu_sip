from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
from distribuidora.models.pedido import PedidoEstado, Pedido, DetallePedido
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer, insert_nuevo_mensaje
from distribuidora.core.gestion_pedido.helper import *
from distribuidora.core.gestion_pedido.forms import NuevoPedido, FormAgregarProducto, \
    ModificarDetallePedido, ActualizarEstadoPedido

pedido = Blueprint('pedido', __name__, template_folder='templates')

def cargar_errores(errores):
    """
    Pasamos el diccionario con todos los errores levantados por Flask
    """
    for key, value in errores.items():
        for v in value:
            flash(v, 'error')

def paginado(page):
    pedidos_todos = db.session.query(Pedido, PedidoEstado).filter(\
        Pedido.usuario_id==current_user.get_id()).\
        filter(PedidoEstado.descripcion_corta!='PCC').\
        filter(Pedido.estado_pedido_id == PedidoEstado.pedido_estado_id).\
        paginate(page, 5, False)
    return pedidos_todos


@pedido.route('/pedido', methods=['GET'])
@login_required
def index():
	return render_template('home_pedido.html', \
			datos=current_user.get_mis_datos(),\
			is_authenticated=current_user.is_authenticated, \
			rol=current_user.get_role(), \
            site='Gestión de Pedido',\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

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
         form=form, site='Gestión de Pedido', \
         sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

@pedido.route('/pedido/consultar', methods=['GET'])
@login_required
def consultar_pedido():
    if current_user.has_role('Cliente'):
        pedido_pcc = get_listado_pedidos_pcc(usuario_id=current_user.get_id())
        if not pedido_pcc:
            pedido_pcc = None
        page = request.args.get('page', 1, type=int)


        return render_template('form_consultar_pedido.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol=current_user.get_role(),\
            site='Gestión de Pedido',\
            pedido_pcc=pedido_pcc,
            pedidos_todos=paginado(page),\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
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
    page = request.args.get('page', 1, type=int)
    return render_template('form_consultar_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido',\
        pedido_pcc=pedido_pcc,\
        pedidos_todos=paginado(page),\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

@pedido.route('/pedido/detalle/modificar', methods=['GET', 'POST'])
@login_required
def modificar_detalle_producto():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    if form.validate_on_submit():
        detalle = request.args.get('detalle_pedido', type=int)
        producto = request.args.get('producto', type=int)
        cantidad = form.cantidad.data
        result = update_detalle_producto(pedido, detalle,\
            cantidad, usuario=current_user.get_role())
        print('%'*100, flush=True)
        print(result, flush=True)
        print('%'*100, flush=True)
        if result:
            flash('Actualizado Correctamente !', 'success')
            if current_user.has_role('Operador'):
                body = 'Modificacion del pedido #{} : - {}'.format(pedido, estado_nuevo)
                receptor = get_pedido_by_id(pedido)[0]['usuario_id']
                print('receptor {}'.format(receptor), flush=True)
                emisor = current_user.get_id()
                data = {
                    "emisor": emisor,
                    "receptor": receptor,
                    "body": body
                }
                resp = insert_nuevo_mensaje(data)
                if resp:
                    flash('Mensaje enviado', 'success')
                else:
                    flash('Algo salió mal, verifique los datos', 'warning')


        else:
            flash('Algo Salió mal !', 'error')
    else:
        cargar_errores(form.errors)

    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido', \
        detalle=detalle,\
        form=form,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

@pedido.route('/pedido/detalle/eliminar', methods=['GET', 'POST'])
@login_required
def eliminar_producto_detalle():
    form = ModificarDetallePedido()
    pedido = request.args.get('pedido', type=int)
    producto_envase_id = request.args.get('producto_envase_id', type=int)
    detalle_id = request.args.get('detalle_pedido', type=int)
    result = eliminar_producto_detalle_pedido(producto_envase_id, detalle_id, pedido)

    if result:

        flash('Producto Eliminado Correctamente !', 'success')
        if current_user.has_role('Operador'):
            # Si el que modifica el pedido es el operador, mando un msj
            body = 'Eliminacion del producto #{producto} del pedido #{pedido}'.format(\
                producto=producto_envase_id, pedido=pedido)
            emisor = current_user.get_id()
            receptor = get_pedido_by_id(pedido)[0]['usuario_id']
            data = {
                "emisor": emisor,
                "receptor": receptor,
                "body": body
                }
            resp = insert_nuevo_mensaje(data)
            if resp:
                flash('Mensaje enviado', 'success')
            else:
                flash('Algo salió mal, verifique los datos', 'warning')
    else:
        flash('Algo Salió mal :( !', 'error')
    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedido.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido', \
        detalle=detalle,\
        form=form,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

@pedido.route('/pedido/confirmar/cliente', methods=['GET', 'POST'])
@login_required
def confirmar_pedido_cliente():
    if current_user.has_role('Cliente'):
        pedido_pcc = request.args.get('pedido_pcc', type=int)
        detalle = get_detalle_pedido(pedido)
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
        estados = get_estados_pedidos_para_operador()

        form = ActualizarEstadoPedido()
        print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
        print(estados)
        form.estado.choices = estados
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
                # Si todo salio bien, debemos informar que hubo
                # una actualización en el estado del pedido
                body = 'Cambio de estado del pedido #{} : - {}'.format(pedido, estado_nuevo)
                receptor = get_pedido_by_id(pedido)[0]['usuario_id']
                print('receptor {}'.format(receptor), flush=True)
                emisor = current_user.get_id()
                data = {
                    "emisor": emisor,
                    "receptor": receptor,
                    "body": body
                }
                resp = insert_nuevo_mensaje(data)
                if resp:
                    flash('Mensaje enviado', 'success')
                else:
                    flash('Algo salió mal, verifique los datos', 'warning')

            else:
                flash('ERROR! El nuevo estado no es posible :(', 'error')

        pedidos = get_listado_pedidos_pco()
        return render_template('listado_pedidos.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol=current_user.get_role(),\
            site='Gestión de Pedido',\
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
            pedidos=pedidos, form=form)
    abort(403)

@pedido.route('/pedido/listar/operador', methods=['GET'])
@login_required
def listar_pedido_operador():
    if current_user.has_role('Operador'):
        pedidos = None
        estados = get_estados_pedidos_para_operador()
        form = ActualizarEstadoPedido()
        print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
        print(estados)
        form.estado.choices = estados
        if current_user.has_role('Operador'):
            pedidos = get_listado_pedidos_pco()
        return render_template('listado_pedidos.html',\
            datos=current_user.get_mis_datos(),\
            is_authenticated=current_user.is_authenticated,\
            rol=current_user.get_role(),\
            site='Gestión de Pedido', \
            pedidos=pedidos, form=form,
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
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
        form=form,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))


@pedido.route('/pedido/listar/detalle/anterior', methods=['GET'])
@login_required
def listar_detalle_pedido_anterior():
    pedido = request.args.get('pedido', type=int)
    estado_pedido = get_estado_actual_pedido(pedido)
    if estado_pedido[0]['descripcion_corta'] in ['PCO']:
        return redirect(url_for('pedido.listar_detalle_pedido', pedido=pedido))

    detalle = get_detalle_pedido(pedido)
    return render_template('detalle_pedidos_anteriores.html',\
        detalle=detalle,\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol=current_user.get_role(),\
        site='Gestión de Pedido',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

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
            return render_template('detalle_pedido.html',\
                detalle=detalle,\
                form=form,\
                datos=current_user.get_mis_datos(),\
                is_authenticated=current_user.is_authenticated,\
                rol=current_user.get_role(),\
                site='Gestión de Pedido',\
                sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
        else:
            flash('ERROR! Ya existe un pedido en curso', 'error')
            return redirect(url_for('pedido.consultar_pedido'))
    abort(403)
