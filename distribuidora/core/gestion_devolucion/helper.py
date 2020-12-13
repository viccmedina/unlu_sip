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

def parser_result_select_field(result):
    salida = list()
    for r in result:
        salida.append(r['descripcion'])
    return salida

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
    estado_devolucion = db.engine.execute(SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION_CORTA.format(descripcion_corta='ECC'))
    
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

def get_devolucion_pedido(devolucion_id):
    print('DEVOLUCION POR PEDIDO PARA OPTENER USUARIO_ID')
    devolucion = db.engine.execute(SELECT_DEVOLUCION.format(devolucion_id=devolucion_id))
    datos = parser_result(devolucion)
    return datos

def get_devolucion_by_pedido(pedido_id):
    devolucion = db.engine.execute(SELECT_DEVOLUCION_BY_PEDIDO.format(pedido_id=pedido_id))
    return parser_result(devolucion)

def check_producto_devolucion(detalle_pedido):
    print('CHECK PRODUCTO DEVOLUCION')
    existe = db.engine.execute(SELECT_DEVOLUCION_BY_DETALLE_PEDIDO.format(detalle_pedido=detalle_pedido))
    result = parser_result(existe)
    print(result)
    return result

def agregar_producto_a_devolucion(motivo, cantidad, devolucion_id, detalle_pedido):
    print('AGREGAR PRODUCTO A LA DEVOLUCION')
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
    estado_devolucion = db.engine.execute(SELECT_DEVOLUCION_CON_ESTADO.format(\
        devolucion_id=devolucion_id))
    estado_devolucion = parser_result(estado_devolucion)
    print('°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°')
    print('devolucion_id : {}'.format(devolucion_id))
    print(estado_devolucion)
    print('°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°')
    update = False
    actual = estado_devolucion[0]['descripcion_corta']
    if  actual == 'ECC' and descripcion_estado_devolucion == 'CPC':
        #actualizamos
        update = True
    elif actual == 'CPC' and descripcion_estado_devolucion == 'R':
        #actualizamos
        update = True
    elif actual == 'CPC' and descripcion_estado_devolucion == 'A':
        #actualizamos
        update = True
    elif actual == 'A' and descripcion_estado_devolucion == 'C':
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
        print('resultado del update: {}'.format(check(result)))

    return update

def insert_into_historial_devolucion(devolucion_id, estado):
    print('AGREGAMOS EN EL HISTORIA DE DEVOLUCION')
    print('ESTADOOOO {}'.format(estado))
    estado_id = get_all_estado_devolucion_by_descripcion_corta(estado)
    print('ESTADOS')
    print(estado_id)
    estado_id = estado_id[0]['estado_devolucion_id']
    result = db.engine.execute(INSERT_INTO_HISTORIAL_DEVOLUCION.format(devolucion_id=devolucion_id, estado_id=estado_id))
    print(check(result))

def get_all_devoluciones_operador():
    print('TODAS LAS DEVOLCIONES PARA VISTA OPERADOR')
    devoluciones = db.engine.execute(SELECT_DEVOLUCION_VISTA_OPERADOR.format(estado='ECC'))
    devoluciones = parser_result(devoluciones)
    print('-------------------------------------------------------------------------------')
    print(devoluciones)
    return devoluciones

def get_detalle_devolucion(devolucion_id):
    print('GET DETALLE DEVOLUCION FULL')
    print('devolucion_id: {} ----'.format(devolucion_id))
    result = db.engine.execute(DETALLE_DEVOLUCION_FULL.format(devolucion_id=devolucion_id))
    detalle = parser_result(result)
    print('detalle: --------------------------- {}'.format(detalle))
    return detalle

def get_all_estado_devolucion():
    print('GET ALL ESTADO DEVOLUCION')
    result = db.engine.execute(SELECT_ALL_ESTADO_DEVOLUCION)
    estados = parser_result_select_field(result)
    print('estados: --------------------------- {}'.format(estados))
    return estados


def get_devolucion_estado_by_descripcion(descripcion):
    result = db.engine.execute(SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION.format(descripcion=descripcion))
    estados = parser_result(result)
    print('estados: |||||||||||||||||||| {}'.format(estados))
    return estados