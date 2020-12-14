from distribuidora import db
from distribuidora.core.gestion_lista_precio.query import *

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp


def consulta_precio_pProductoMarcaUMedida(producto,marca,umedida):
    p = None
    mar = db.engine.execute(CONSULTAR_MARCA.format(marca=marca))
    for row in mar:
        m = row.marca_id
    umed = db.engine.execute(CONSULTAR_U_MEDIDA.format(umedida=umedida))
    for row in umed:
        um = row.unidad_medida_id
    pro = db.engine.execute(CONSULTAR_PRODUCTO.format(producto=producto,marca=m,umedida=um))
    for row in pro:
        p = row.producto
    if p == None:
        return None
    else:
        precio = db.engine.execute(CONSULTAR_PRECIO.format(producto=p))

    return parser_result(precio)

def consultar_precio_pProductoMarcaUMedida(producto,marca,umedida):
    p = None
    mar = db.engine.execute(CONSULTAR_MARCA.format(marca=marca))
    for row in mar:
        m = row.marca_id
    umed = db.engine.execute(CONSULTAR_U_MEDIDA.format(umedida=umedida))
    for row in umed:
        um = row.unidad_medida_id
    pro = db.engine.execute(CONSULTAR_PRODUCTO.format(producto=producto,marca=m,umedida=um))
    for row in pro:
        p = row.producto
    if p == None:
        return None
    else:
        precio = db.engine.execute(CONSULTAR_PRECIO.format(producto=p))


    return precio


def agregar_precio_pProductoMarcaUMedida(producto,marca,umedida,precio,fecha):
    mar = db.engine.execute(CONSULTAR_MARCA.format(marca=marca))
    for row in mar:
        m = row.marca_id
    umed = db.engine.execute(CONSULTAR_U_MEDIDA.format(umedida=umedida))
    for row in umed:
        um = row.unidad_medida_id
    pro = db.engine.execute(CONSULTAR_PRODUCTO.format(producto=producto,marca=m,umedida=um))
    for row in pro:
        p = row.producto
    if p == None:
        return None
    db.engine.execute(AGREGAR_PRECIO.format(fecha=fecha))
    id_precio = db.engine.execute(CONSULTAR_ID_PRECIO.format(fecha=fecha))
    for row in id_precio:
        print("precio id es {}".format(row.precio_id))
        db.engine.execute(AGREGAR_PRECIO_PRODUCTO.format(producto=p,precio=precio,fecha=fecha,id=row.precio_id))

def modificarPrecio(precio,producto):
    print("precio {}".format(precio))
    db.engine.execute(ACTUALIZAR_PRECIO.format(producto=producto,precio=precio))


def modificarFecha(fecha,producto,olddate):
    id_precio = db.engine.execute(CONSULTAR_ID_PRECIO.format(fecha=olddate))
    for row in id_precio:
        print("precio {}".format(row.precio_id))
        print("producto {}".format(producto))
        db.engine.execute(ACTUALIZAR_FECHA.format(fecha=fecha,id=row.precio_id))
        db.engine.execute(ACTUALIZAR_FECHA_PP.format(producto=producto,fecha=fecha,id=row.precio_id))

def consultaListaPreciosExportar():
    list = []
    resultado = db.engine.execute(PRODUCTOS_TO_EXPORT)
    return parser_result(resultado)



def consultarFechaData():
    fecha = db.engine.execute(AGREGAR_PRECIO_PRODUCTO.format(producto=p,precio=precio,fecha=fecha,id=row.precio_id))

def modificarPrecioFecha(fecha,precio,producto,olddate):
    id_precio = db.engine.execute(CONSULTAR_ID_PRECIO.format(fecha=olddate))
    for row in id_precio:
        db.engine.execute(ACTUALIZAR_FECHA_PRECIO.format(fecha=fecha,id=row.precio_id))
        db.engine.execute(ACTUALIZAR_FECHA_PRECIO_LISTA.format(producto=producto,fecha=fecha,id=row.precio_id,precio=precio))
