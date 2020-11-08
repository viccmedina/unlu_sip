from distribuidora import db
from distribuidora.core.gestion_producto.query import LISTAR_PRODUCTOS

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
