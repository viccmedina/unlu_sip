from distribuidora import db
from distribuidora.core.gestion_pedido.query import *

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def get_estado_pedido_id(descripcion_corta):
    """
    Dado una descripción corta de uno de los estados de los pedidos,
    retornaremos su id.
    """

    result = db.engine.execute(CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID.format(\
        descripcion_corta=descripcion_corta))
    return parser_result(result)

def check_nuevo_pedido(cliente, estado):
    """
    Dada la solicitud de un nuevo pedido vamos a verificar si no existen pedidos
    creados cuyo estado sea PCC (Pendiente Confirmación Cliente). Solamente
    admitimos un pedido sin confirmar por vez.
    """
    return True

def crear_nuevo_pedido(cliente, estado):
    """
    Dado un id de cliente y un estado, vamos a crear un nuevo pedido con el
    estado pasado por parametro como estado inicial
    """
    if not check_nuevo_pedido(cliente, estado):
        return False
    else:

        result = db.engine.execute(INSERT_NUEVO_PEDIDO.format(\
            usuario_id=cliente))
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

def insert_into_detalle_pedido(pedido_id, producto_id, cantidad=1):
    """
    Dado el nro de pedido, el producto y la cantidad insertamos dentro del
    detalle del pedido.
    """
    result = db.engine.execute(INSERT_INTO_DETALLE_PEDIDO.format(\
        pedido_id=pedido_id, producto_id=producto_id, cantidad=cantidad))

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

def update_detalle_producto(detalle, cantidad):
    result = db.engine.execute(UPDATE_CANTIDAD_DETALLE_PEDIDO.format(\
        detalle_id=detalle, cantidad=cantidad))
    print(result.rowcount, flush=True)
    if result.rowcount == 1 :
        return True
    else:
        return False

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
