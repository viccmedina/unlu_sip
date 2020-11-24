from distribuidora import db
from distribuidora.core.gestion_producto.query import *

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def lista_de_productos():
    resultado = db.engine.execute(LISTAR_ALL_PRODUCTOS)
    return parser_result(resultado)

def get_lista_productos():
	"""
	Devolvemos todos los productos que tenemos cargados en la base.
	"""
	result = db.engine.execute(LISTAR_PRODUCTOS)
	return parser_result(result)

def get_producto_by_descripcion_marca(producto, marca):
    """
    Dado la descripcion de un producto y su marca devolvemos su id
    """
    result = db.engine.execute(PRODUCTO_BY_DESCRIPCION_MARCA.format(\
        producto=producto, marca=marca))
    return parser_result(result)

def get_producto_envase_by_producto_id(producto_id):
    """
    Devolvemos todas las versiones del produto. Es decir,
    si solicitamos el producto Harina, devolvemos el mismo en todos los envases
    cargados en el sistema junto con información asociada:
    - precio,
    - marca,
    - unidad_medida
    """
    result = db.engine.execute(PRODUCTO_ENVASE_BY_PRODUCTO_ID.format(\
        producto_id=producto_id))
    return parser_result(result)

def get_producto_id_from_producto_envase(producto_envase_id):
    result = db.engine.execute(PRODUCTO_ID_FROM_PRODUCTO_ENVASE.format(\
        producto_envase_id=producto_envase_id))
    return parser_result(result)
