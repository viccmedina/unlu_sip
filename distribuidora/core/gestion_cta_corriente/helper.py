from distribuidora import db
from distribuidora.core.gestion_cta_corriente.query import SELECT_TIPO_MOVIMIENTOS, CONSULTA_MOVIMIENTOS_CTA_CORRIENTE, CONSULTAR_NRO_CUENTA_CORRIENTE, SELECT_ID_TIPO_MOVIMIENTO

def get_tipos_movimientos():
    """
    Realiza la consulta a la base para obtener los tipos de movimientos.
    Nos devolverá una lista del tipo:
    ['Deuda', 'Pago', 'Reembolso']
    """
    #result = db.engine.execute(SELECT_TIPO_MOVIMIENTOS)
    #resp = []
    #for row in result:
    #    resp.append(row[0])
    #return resp
    pass

def get_id_tipos_movimientos(descripcion):
    """
    Dada la descripcion del tipo de movimiento,
    devolvemos el id.
    """
    result = db.engine.execute(SELECT_ID_TIPO_MOVIMIENTO.format(\
        tipo_movimiento=descripcion))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def get_nro_cuenta_corriente(nro_cliente):
    """
    Dado un nro de cliente nos devolverá su nro de cuenta corriente.
    """
    #result = db.engine.execute(CONSULTAR_NRO_CUENTA_CORRIENTE.format(nro_cliente=nro_cliente))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def get_consulta_movimientos(fecha_desde, fecha_hasta, nro_cliente):
    """
    Dado los siguientes parámetros:
    - fecha_desde,
    - fecha_hasta
    - nro_cliente

    vamos a consultar todos los movimientos de la cta corriente de ese Cliente
    dentro de ese rango de fechas.
    """
    result = db.engine.execute(CONSULTA_MOVIMIENTOS_CTA_CORRIENTE.format(\
        fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, \
        nro_cliente=nro_cliente))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp
