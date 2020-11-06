from distribuidora import db
from distribuidora.core.gestion_pedido.query import CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID, \
    INSERT_NUEVO_PEDIDO, INSERT_NUEVO_ESTADO_PEDIDO, SELECT_ID_ULTIMO_PEDIDO

def get_estado_pedido_id(descripcion_corta):
    """
    Dado una descripción corta de uno de los estados de los pedidos,
    retornaremos su id.
    """

    result = db.engine.execute(CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID.format(\
        descripcion_corta=descripcion_corta))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def crear_nuevo_pedido(cliente, estado):
    """
    Dado un id de cliente y un estado, vamos a crear un nuevo pedido con el
    estado pasado por parametro como estado inicial
    """
    result = db.engine.execute(INSERT_NUEVO_PEDIDO.format(\
        usuario_id=cliente))
    #result = db.engine.execute(INSERT_NUEVO_ESTADO_PEDIDO.format(\
    #    pedido_id=cliente, pedido_estado_id=estado))
    # resp = []
    # print(result, flush=True)
    # if result is not None:
    #     for row in result:
    #         resp.append(dict(row))
    #     return resp

def get_ultimo_pedido_id(usuario_id):
    """
    Dado un id de usuario, vamos a obtener el id del último pedido generado.
    """
    result = db.engine.execute(SELECT_ID_ULTIMO_PEDIDO.format(\
        usuario_id=cliente))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp
