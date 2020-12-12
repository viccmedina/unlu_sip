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


def get_consulta_stock(fecha_desde, fecha_hasta):
    list = []
    all_productos = db.engine.execute(CONSULTAR_PRODUCTOS)
    for row in all_productos:
        datos = db.engine.execute(CONSULTA_MOVIMIENTOS_STOCK.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.producto_envase_id))
        for row in datos:
            if row.stock == None:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                datos = db.engine.execute(CONSULTA_STOCK_REAL.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.pei))
=======
                datos = db.engine.execute(CONSULTA_STOCK_REAL.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.peid))
>>>>>>> Stashed changes
=======
                datos = db.engine.execute(CONSULTA_STOCK_REAL.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.peid))
>>>>>>> Stashed changes
                for r in datos:
                    list.append(r)
            else:
                list.append(row)
    return list


def get_consulta_lista_precios(fecha_desde, fecha_hasta):
    list = []
    pass


def get_consulta_productos(fecha_desde, fecha_hasta):
    list = []
    all_productos = db.engine.execute(CONSULTAR_PRODUCTOS)
    for row in all_productos:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        datos = db.engine.execute(CONSULTA_STOCK_REAL.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.producto_envase_id))
=======
        datos = db.engine.execute(CONSULTA_MOVIMIENTOS_STOCK.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.producto_envase_id))
>>>>>>> Stashed changes
=======
        datos = db.engine.execute(CONSULTA_MOVIMIENTOS_STOCK.format(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,productoEnvase=row.producto_envase_id))
>>>>>>> Stashed changes
        for row in datos:
            list.append(row)
    return list
