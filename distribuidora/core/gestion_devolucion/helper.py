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


def check(result):
    if result.rowcount == 1 :
        return True
    else:
        return False

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

def generar_nueva_devolucion(pedido_id):
    estado_devolucion = db.engine.execute(SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION.format(descripcion_corta='EC'))
    
    estado_devolucion = parser_result(estado_devolucion)
    print('ESTADO DEVOLUCION ---- {}'.format(estado_devolucion))
    result = db.engine.execute(INSERT_INTO_DEVOLUCION.format(pedido_id=pedido_id,\
        estado_devolucion_id=estado_devolucion[0]['estado_devolucion_id']))
    return check(result)

def get_all_devoluciones(usuario_id):
    devoluciones = db.engine.execute(SELECT_ALL_DEVOLUCIONES.format(usuario_id=usuario_id))
    return parser_result(devoluciones)