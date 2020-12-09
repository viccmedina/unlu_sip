from distribuidora import db
from distribuidora.core.gestion_devolucion.query import *


def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def parser_resultINT(result):
    resp = []
    for row in result:
        print(type(row))
        resp.append(int(row['pedido']))
    return resp


def buscar_pedido_id(user):
    print("usuario es {}".format(user))
    resp = []
    estado_id = db.engine.execute(GET_ESTADO_PEDIDO)
    for row in estado_id:
        e= row.pedido_estado_id
    print("p es {}".format(e))
    result = db.engine.execute(LISTAR_PEDIDOS.format(user=user,ep=e))
    for row in result:
        if row.dias < 10:
            print("es mayor a 10")
            resp.append(row.pedido)
        else:
            print("no es mayor a 10")

    return resp

def detalle_pedidos(pedidos_id):
    resp = []
    print("p es {}".format(pedidos_id))
    detalles_ped = db.engine.execute(LIST_PEDIDO_DETALLE.format(p_id=pedidos_id))
    for row in detalles_ped:
        prod = db.engine.execute(LIST_PRODUCTO_DETALLE.format(producto=row.producto_envase_id))
        for row in prod:
            resp.append(row)

    return resp
