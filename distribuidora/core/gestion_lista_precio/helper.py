from distribuidora import db
from distribuidora.core.gestion_lista_precio.query import *

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp


def consulta_precio_pProductoMarcaUMedida(producto,marca,umedida):
    mar = db.engine.execute(CONSULTAR_MARCA.format(marca=marca))
    for row in mar:
        m = row.marca_id
    umed = db.engine.execute(CONSULTAR_U_MEDIDA.format(umedida=umedida))
    for row in umed:
        um = row.unidad_medida_id
    pro = db.engine.execute(CONSULTAR_PRODUCTO.format(producto=producto,marca=m,umedida=um))
    for row in pro:
        p = row.producto

    precio = db.engine.execute(CONSULTAR_PRECIO.format(producto=p))

    return parser_result(precio)
