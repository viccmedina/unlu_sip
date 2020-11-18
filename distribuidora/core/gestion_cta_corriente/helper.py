from distribuidora import db
from distribuidora.core.gestion_cta_corriente.query import SELECT_TIPO_MOVIMIENTOS, CONSULTA_MOVIMIENTOS_CTA_CORRIENTE, \
CONSULTAR_NRO_CUENTA_CORRIENTE, SELECT_ID_TIPO_MOVIMIENTO, INSERT_MOV_CTA_CORRIENTE, CONSULTAR_SALDO

def get_tipos_movimientos():
    """
    Realiza la consulta a la base para obtener los tipos de movimientos.
    Nos devolverá una lista del tipo:
    ['Deuda', 'Pago', 'Reembolso']
    """
    result = db.engine.execute(SELECT_TIPO_MOVIMIENTOS)
    resp = []
    for row in result:
       resp.append(row[0])
    return resp
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
    nro_cta = None
    result = db.engine.execute(CONSULTAR_NRO_CUENTA_CORRIENTE.format(nro_cliente=nro_cliente))
    resp = []
    for row in result:
        nro_cta = row['cuenta_corriente_id']

    if nro_cta is None:
        nro_cta = -999

    return nro_cta

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

def new_mov_cta_corriente(nro_cta,tipo_mov,user,monto):
    id_t_mov = db.engine.execute(SELECT_ID_TIPO_MOVIMIENTO.format(tipo_movimiento=tipo_mov))
    for row in id_t_mov:
        t_movimiento = row['id']

    desc = "Es un/a {}".format(tipo_mov)
    #si es deuda ingreso negativo

    print(" t mov : {}".format(t_movimiento))
    if t_movimiento == 2 :
        saldo = float(monto * (-1))
        db.engine.execute(INSERT_MOV_CTA_CORRIENTE.format(n_cta=nro_cta, t_mov=t_movimiento, \
        user=user,descripcion=desc,monto=saldo))
    else:
        print("agregamos movimientos")
        db.engine.execute(INSERT_MOV_CTA_CORRIENTE.format(n_cta=nro_cta, t_mov=t_movimiento, \
        user=user,descripcion=desc,monto=monto))


def consulta_saldo(nro_cta):
    saldo = db.engine.execute(CONSULTAR_SALDO.format(nro_cta=nro_cta))

    resp = []
    for row in saldo:
        a = row['saldo']
        print("asdsasdasdasdasdasdadsa {}".format(a))
        resp.append(dict(row))
    return resp
