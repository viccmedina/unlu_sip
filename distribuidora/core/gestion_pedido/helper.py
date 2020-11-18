from distribuidora import db
from distribuidora.core.gestion_pedido.query import *

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def check(result):
    if result.rowcount == 1 :
        return True
    else:
        return False

def get_estado_pedido_id(descripcion_corta):
    """
    Dado una descripción corta de uno de los estados de los pedidos,
    retornaremos su id.
    """

    result = db.engine.execute(CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID.format(\
        descripcion_corta=descripcion_corta))
    return parser_result(result)

def get_estado_pedido_id_descripcion(descripcion):
    result = db.engine.execute(SELECT_ESTADO_PEDIDO_DESCRIPCION.format(descripcion=descripcion))
    result = parser_result(result)
    return result

def get_estados_pedidos_para_operador():
    result = db.engine.execute(SELECT_PEDIDOS_ESTADOS_FOR_OPERADOR)
    result = parser_result(result)
    print('estados: {}'.format(result), flush=True)
    e = list()
    for r in result:
        e.append(r['descripcion'])
    return e

def check_nuevo_pedido(cliente, estado):
    """
    Dada la solicitud de un nuevo pedido vamos a verificar si no existen pedidos
    creados cuyo estado sea PCC (Pendiente Confirmación Cliente). Solamente
    admitimos un pedido sin confirmar por vez.
    """
    return True

def update_estado_pedido_tbl_pedido(pedido_id, estado_pedido_id):
    """
    Cada vez que se actualiza el estado del pedido mandamos a actualizar el estado
    tanto en la tbl de historial como en la tbl de pedido.
    """
    result = db.engine.execute(UPDATE_PEDIDO_ESTADO.format(pedido_id=pedido_id,\
        estado_pedido_id=estado_pedido_id))
    return check(result)


def crear_nuevo_pedido(cliente, estado):
    """
    Dado un id de cliente y un estado, vamos a crear un nuevo pedido con el
    estado pasado por parametro como estado inicial
    """
    if not check_nuevo_pedido(cliente, estado):
        return False
    else:

        result = db.engine.execute(INSERT_NUEVO_PEDIDO.format(\
            usuario_id=cliente, estado_pedido_id=estado))
        pedido_id = db.engine.execute(SELECT_ID_ULTIMO_PEDIDO.format(\
            usuario_id=cliente))
        print('#'*80)
        pedido_id = parser_result(pedido_id)
        result = db.engine.execute(INSERT_NUEVO_HISTORIAL_PEDIDO_ESTADO.format(\
            pedido_estado_id=estado, pedido_id=pedido_id[0]['pedido_id']))
        return True

def get_cantidad_estados_pedido(pedido_id):
    result = db.engine.execute(CANTIDAD_ESTADOS_DEL_PEDIDO.format(\
        pedido_id=pedido_id))
    result = parser_result(result)
    print(result, flush=True)
    return result[0]['cantidad']

def get_ultimo_pedido_id(usuario_id):
    """
    Dado un id de usuario, vamos a obtener el id del último pedido generado.
    """
    result = db.engine.execute(SELECT_ULTIMO_PEDIDO_ID_POR_CLIENTE.format(\
        usuario_id=usuario_id))
    result = parser_result(result)
    print('='*90, flush=True)
    print(result, flush=True)
    print('='*90, flush=True)
    return result[0]['pedido_id']

def get_detalle_pedido(pedido_id):
    result = db.engine.execute(LISTAR_DETALLE_PEDIDO.format(pedido_id=pedido_id))
    result = parser_result(result)
    print('='*90, flush=True)
    print(result, flush=True)
    print('='*90, flush=True)
    return result

def check_estado_actual_pedido(pedido_id):
    """
    Dado un identificador de pedido, devolvemos su estado actual.
    """
    result = db.engine.execute(CANTIDAD_ESTADOS_DEL_PEDIDO.format(pedido_id=pedido_id))
    result = parser_result(result)
    print('7'*90, flush=True)
    print(result, flush=True)
    print('7'*90, flush=True)
    return result

def insert_into_detalle_pedido(pedido_id, producto_envase_id, cantidad=1):
    """
    Dado el nro de pedido, el producto y la cantidad insertamos dentro del
    detalle del pedido.
    """

    result = db.engine.execute(INSERT_INTO_DETALLE_PEDIDO.format(\
        pedido_id=pedido_id, producto_envase_id=producto_envase_id, cantidad=cantidad))
    return check(result)

def get_listado_pedidos_pco():
    """
    Devolvemos todos los pedidos cuyo estado sea PCO (Pendiente Confirmación
    por Operador)
    """
    result = db.engine.execute(SELECT_PEDIDOS_ESTADO_PCO)
    result = parser_result(result)
    print('='*90, flush=True)
    print(result, flush=True)
    print('='*90, flush=True)
    return result

def get_listado_pedidos_pcc(usuario_id):
    result = db.engine.execute(SELECT_PEDIDOS_ESTADO_PCC.format(\
        usuario_id=usuario_id))
    result = parser_result(result)
    print('='*90, flush=True)
    print(result, flush=True)
    print('='*90, flush=True)
    return result

def update_detalle_producto(pedido_id, detalle, cantidad):
    if get_cantidad_estados_pedido(pedido_id) < 3 :
        result = db.engine.execute(UPDATE_CANTIDAD_DETALLE_PEDIDO.format(\
            detalle_id=detalle, cantidad=cantidad))
        print(result.rowcount, flush=True)
        return check(result)
    else:
        return False

def actualizar_pedido_estado_por_operador(pedido, estado_nuevo, estado_actual):
    estado_id_nuevo = get_estado_pedido_id_descripcion(estado_nuevo)[0]
    print('estado_id_nuevo --> {}'.format(estado_id_nuevo), flush=True)
    estado_id_actual = get_estado_pedido_id_descripcion(estado_actual)[0]
    execute = True
    if estado_id_actual['descripcion_corta'] == 'PCO' and estado_id_nuevo['descripcion_corta'] in ['EP', 'RPO']:
        print('ESTADO VALIDO, PODEMOS ACTUALIZAR', flush=True)
    elif estado_id_actual['descripcion_corta'] == 'EP' and estado_id_nuevo['descripcion_corta'] == 'EC':
        print('ESTADO VALIDO, PODEMOS ACTUALIZAR', flush=True)
    elif estado_id_actual['descripcion_corta'] == 'EC' and estado_id_nuevo['descripcion_corta'] in ['D', 'E']:
        print('ESTADO VALIDO, PODEMOS ACTUALIZAR', flush=True)
    else:
        print('ERROR', flush=True)
        execute = False
    if execute:
        result = db.engine.execute(INSERT_NUEVO_HISTORIAL_PEDIDO_ESTADO.format(\
            pedido_id=pedido, pedido_estado_id=estado_id_nuevo['pedido_estado_id']))
        update_detalle_producto(pedido, estado_id_nuevo['pedido_estado_id'])
        query = check(result)
        if query:
            if estado_id_nuevo['descripcion_corta'] == 'EP':
                pass
                #agregar movimiento cta corriente
                #descontar del stock

        return check(result)
    else:
        return execute

def actualizar_estado_pedido(pedido, estado):
    """
    Dado un nro de pedido y un estado, actualizamos
    el estado de dicho pedido.
    """
    print('ACTUALIZAR!!', flush=True)
    estado_id = db.engine.execute(CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID.format(descripcion_corta=estado))
    estado_id = parser_result(estado_id)
    print(estado_id, flush=True)
    result = db.engine.execute(INSERT_NUEVO_HISTORIAL_PEDIDO_ESTADO.format(\
        pedido_id=pedido, pedido_estado_id=estado_id[0]['pedido_estado_id']))
    return check(result)

def eliminar_producto_detalle_pedido(producto_envase_id, detalle_id, pedido_id):
    if get_cantidad_estados_pedido(pedido_id) < 3 :
        result = db.engine.execute(DELETE_PRODUCTO_FROM_DETALLE_PEDIDO.format(\
            detalle_id=detalle_id, producto_envase_id=producto_envase_id))
        print(result.rowcount, flush=True)
        return check(result)
    else:
        return False

def anular_pedido_por_cliente(pedido_id):
    """
    Dado un identificador de pedido, vamos a eliminarlo.
    Primero debemos comprobar que tiene el estado PCC. Caso contrario no se podrá
    eliminar.
    """
    pedido = db.engine.execute(SELECT_PEDIDO.format(pedido_id=pedido_id))
    pedido = parser_result(pedido)
    print(pedido, flush=True)
    if pedido[0]['descripcion_corta'] == 'PCC':
        print('PODEMOS ANULAR EL PEDIDO', flush=True)
        delete = db.engine.execute(DELETE_PEDIDO_BY_CLIENTE.format(pedido_id=pedido_id))
        return check(delete)
    else:
        return False
