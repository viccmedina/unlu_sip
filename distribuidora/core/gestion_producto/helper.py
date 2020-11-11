from distribuidora import db
from distribuidora.core.gestion_producto.query import LISTAR_PRODUCTOS, \
    PRODUCTO_ENVASE_BY_PRODUCTO_ID

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp



def get_lista_productos():
	"""
	Devolvemos todos los productos que tenemos cargados en la base.
	"""
	result = db.engine.execute(LISTAR_PRODUCTOS)
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
