from distribuidora import db
from distribuidora.core.gestion_cta_corriente.query import *

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

def get_tipos_movimientos():
    """
    Realiza la consulta a la base para obtener los tipos de movimientos.
    Nos devolverá una lista del tipo:
    ['Deuda', 'Pago', 'Reembolso']
    """
    result = db.engine.execute(SELECT_TIPO_MOVIMIENTOS)
    return parser_result(result)

def get_id_tipos_movimientos(descripcion):
    """
    Dada la descripcion del tipo de movimiento,
    devolvemos el id.
    """
    result = db.engine.execute(SELECT_ID_TIPO_MOVIMIENTO.format(\
        tipo_movimiento=descripcion))
    return parser_result(result)

def get_nro_cuenta_corriente(nro_cliente):
    """
    Dado un nro de cliente nos devolverá su nro de cuenta corriente.
    """
    nro_cta = None
    result = db.engine.execute(CONSULTAR_NRO_CUENTA_CORRIENTE.format(nro_cliente=nro_cliente))
    print('!!!!!!!!!!!!!!!!!!!!!!')
    result = parser_result(result)
    print(result, flush=True)
    return result

def get_consulta_movimientos(fecha_desde, fecha_hasta, nro_cliente):
    """
    Dado los siguientes parámetros:
    - fecha_desde,
    - fecha_hasta
    - nro_cliente

    vamos a consultar todos los movimientos de la cta corriente de ese Cliente
    dentro de ese rango de fechas.
    """
    print('FECHAS ---')
    print(fecha_hasta)
    print(type(fecha_hasta))
    result = db.engine.execute(CONSULTA_MOVIMIENTOS_CTA_CORRIENTE_BY_OPERADOR.format(\
        fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, \
        nro_cliente=nro_cliente))
    resp = parser_result(result)

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(resp)
    return resp

def new_mov_cta_corriente(nro_cta,tipo_mov,user,monto):
    id_t_mov = db.engine.execute(SELECT_ID_TIPO_MOVIMIENTO.format(tipo_movimiento=tipo_mov))
    for row in id_t_mov:
        t_movimiento = row['id']

    desc = "Es un/a {}".format(tipo_mov)
    #si es deuda ingreso negativo

    print(" t mov : {}".format(t_movimiento))
    if t_movimiento == 2 :
        saldo = float(monto)
        query = db.engine.execute(INSERT_MOV_CTA_CORRIENTE.format(n_cta=nro_cta, t_mov=t_movimiento, \
            user=user,descripcion=desc,monto=saldo))
    else:
        print("agregamos movimientos")
        query = db.engine.execute(INSERT_MOV_CTA_CORRIENTE.format(n_cta=nro_cta, t_mov=t_movimiento, \
            user=user,descripcion=desc,monto=monto))

    return check(query)




def consultaCtaCorrienteExportar():

    list = []
    id = None
    usuarios =  db.engine.execute(CONSULT_ALL_USERS)
    for row in usuarios:
        id = row.id
        saldoCC = db.engine.execute(CONSULTAR_MONTO_CC.format(user=row.id))#lo que debe
        saldoCP = db.engine.execute(CONSULTAR_MONTO_CP.format(user=row.id))# lo oque pago
        print("usuario {}".format(row.id))
        for row in saldoCC:
            if(row.saldoCC != None):
                scc= float(row.saldoCC)
                print("scc {}".format(scc))
            else:
                scc = 0
        for row in saldoCP:
            if(row.saldoCP != None):
                scp= float(row.saldoCP)
                print("scc {}".format(scp))
            else:
                scp = 0

        resta =   scc -   scp # resto deuda - pagos
        print("resta {}".format(resta))
        datos = db.engine.execute(CONSULTA_MOVIMIENTOS_CTA_CORRIENTE.format(user=id))# constultos el resto de los valores
        for row in datos:
            print(row)
    return parser_result(datos)


def consulta_saldo_aparte(nro_cta):
    saldito = None
    salDeuda = db.engine.execute(CONSULTAR_SALDO_DEUDA.format(nro_cta=nro_cta))
    for row in salDeuda:
        d= row[0]
    salPagos = db.engine.execute(CONSULTAR_SALDO_PAGOS.format(nro_cta=nro_cta))
    for row in salPagos:
        p= row[0]
    print("deudas {}".format(d))
    print("pagos {}".format(p))
    if p is None and d is not None:
        saldito = d * (-1)
    elif d is None and p is not None:
        saldito = p
    elif d is not None and p is not None:
        saldito =  p - d
    else:
        saldito = 0

    return saldito


def consulta_saldo(nro_cta):
    saldo = db.engine.execute(CONSULTAR_SALDO.format(nro_cta=nro_cta))

    return parser_result(saldo)



def actualizar_estado_comprobante_pago(monto, cliente):
    """
    Dado un nro de usuario y el monto asociado a un movimiento de cuenta corriente,
    vamos a comprobar si podemos dar como pago un comprobante de pago.
    """
    comprobantes = db.engine.execute(SELECT_COMPROBANTES_PAGO_ADEUDA.format(\
        estado='Adeuda', usuario_id=cliente, monto=monto))
    comprobantes = parser_result(comprobantes)
    print(type(comprobantes), flush=True)
    print(comprobantes, flush=True)
    query = False
    if len(comprobantes) > 0:
        update_comprobante = db.engine.execute(UPDATE_ESTADO_COMPROBANTE.format(\
            estado=2,comprobante_id=comprobantes[0]['comprobante_id']))
        query = check(update_comprobante)
    return query
