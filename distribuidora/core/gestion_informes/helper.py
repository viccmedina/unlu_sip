from distribuidora import db
from distribuidora.core.gestion_informes.query import *


def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp


def get_consulta_movimientos(fecha_desde, fecha_hasta):
    list = []
    all_usuarios = db.engine.execute(CONSULTAR_USUARIO)
    for row in all_usuarios:
        datos = db.engine.execute(CONSULTA_MOVIMIENTOS_CTA_CORRIENTE.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,user=row.id))
        for row in datos:
            list.append(row)
    return list


def get_consulta_devoluciones(fecha_desde, fecha_hasta):
    list = []
    pass


def get_consulta_stock():
    list = []
    all_productos = db.engine.execute(CONSULTAR_PRODUCTOS)
    for row in all_productos:
        datos = db.engine.execute(CONSULTA_MOVIMIENTOS_STOCK.format(productoEnvase=row.producto_envase_id))
        for row in datos:
            if row.stock == None:
                datos = db.engine.execute(CONSULTA_STOCK_REAL.format(productoEnvase=row.peid))
                for r in datos:
                    list.append(r)
            else:
                list.append(row)
    return list


def get_consulta_lista_precios(id=id):
    list = []
    all_productos = db.engine.execute(CONSULTAR_PRODUCTOS)
    for row in all_productos:
        precios = db.engine.execute(CONSULTA_LISTA_PRECIOS.format(id=id,productoEnvase=row.producto_envase_id))
        for row in precios:
            list.append(row)

    return list


def get_consulta_productos(fecha_desde, fecha_hasta):
    list = []
    all_productos = db.engine.execute(CONSULTAR_PRODUCTOS)
    for row in all_productos:
        datos = db.engine.execute(CONSULTAR_PRODUCTOS_ALL.format(desde=fecha_desde, hasta=fecha_hasta,productoEnvase=row.producto_envase_id))
        for row in datos:
            list.append(row)
    return list

def constultar_id_precio(id):
    fechas = db.engine.execute(CONSULTA_FECHAS_PRECIOS_FOR_PRECIOS.format(id=id))
    return fechas
