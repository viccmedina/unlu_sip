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
    estado_devolucion = db.engine.execute(SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION.format(descripcion_corta='ECC'))
    
    estado_devolucion = parser_result(estado_devolucion)
    print('ESTADO DEVOLUCION ---- {}'.format(estado_devolucion))
    result = db.engine.execute(INSERT_INTO_DEVOLUCION.format(pedido_id=pedido_id,\
        estado_devolucion_id=estado_devolucion[0]['estado_devolucion_id']))
    return check(result)

def get_all_devoluciones(usuario_id):
    devoluciones = db.engine.execute(SELECT_ALL_DEVOLUCIONES.format(usuario_id=usuario_id))
    return parser_result(devoluciones)

def get_all_motivo_by_descripcion(motivo):
    motivos = db.engine.execute(SELECT_ALL_MOTIVOS_BY_DESCRIPCION.format(descripcion=motivo))
    return parser_result(motivos)


def get_devolucion_by_pedido(pedido_id):
    devolucion = db.engine.execute(SELECT_DEVOLUCION_BY_PEDIDO.format(pedido_id=pedido_id))
    return parser_result(devolucion)

def check_producto_devolucion(detalle_pedido):
    existe = db.engine.execute(SELECT_DEVOLUCION_BY_DETALLE_PEDIDO.format(detalle_pedido=detalle_pedido))
    print('oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
    result = parser_result(existe)
    print(result)
    print('oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
    return result

def agregar_producto_a_devolucion(motivo, cantidad, devolucion_id, detalle_pedido):
    print('producto agregado!')
    print('mmmmmmmmmmmmmmmmmmmmm')
    print(motivo)
    motivo = get_all_motivo_by_descripcion(motivo)
    print(motivo)
    result = db.engine.execute(INSERT_INTO_DETALLE_DEVOLUCION.format(motivo_id=motivo[0]['motivo_devolucion_id'],\
        devolucion_id=devolucion_id, detalle_pedido_id=detalle_pedido, cantidad=cantidad))
    return check(result)
  

def get_all_estado_devolucion_by_descripcion_corta(descripcion_estado_devolucion):
    result = db.engine.execute(SELECT_ALL_ESTADO_DEVOLUCION_BY_DESCRIPCION_CORTA.format(\
        descripcion_corta=descripcion_estado_devolucion))
    result = parser_result(result)
    return result

def update_estado_devolucion(devolucion_id, descripcion_estado_devolucion):
    print('update estado descripcion')
    estado_devolucion = db.engine.execute(SELECT_DEVOLUCION_CON_ESTADO.format(devolucion_id=devolucion_id))
    estado_devolucion = parser_result(estado_devolucion)
    print('°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°')
    print('devolucion_id : {}'.format(devolucion_id))
    print(estado_devolucion)
    print('°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°')
    update = False
    if estado_devolucion[0]['descripcion_corta'] == 'ECC' and descripcion_estado_devolucion == 'CPC':
        #actualizamos
        update = True
    elif estado_devolucion[0]['descripcion_corta'] == 'CPC' and descripcion_estado_devolucion == 'R':
        #actualizamos
        update = True
    elif estado_devolucion[0]['descripcion_corta'] == 'CPC' and descripcion_estado_devolucion == 'A':
        #actualizamos
        update = True

    if update:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(descripcion_estado_devolucion)
        estado = get_all_estado_devolucion_by_descripcion_corta(descripcion_estado_devolucion)
        print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
        print(estado)
        result = db.engine.execute(UPDATE_ESTADO_DEVOLUCION.format(devolucion_id=devolucion_id,\
            estado=estado[0]['estado_devolucion_id']))

    return update

def insert_into_historial_devolucion(devolucion_id, estado):
    print('AGREGAMOS EN EL HISTORIA DE DEVOLUCION')
    estado_id = get_all_estado_devolucion_by_descripcion_corta(estado)
    print('ESTADOSSSSSSSSSS')
    print(estado_id)
    estado_id = estado_id[0]['estado_devolucion_id']
    result = db.engine.execute(INSERT_INTO_HISTORIAL_DEVOLUCION.format(devolucion_id=devolucion_id, estado_id=estado_id))
    print(check(result))
