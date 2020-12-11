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
