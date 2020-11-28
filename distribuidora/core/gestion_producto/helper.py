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



def consultar_id_producto(producto):
    b = False
    result = db.engine.execute(CONSULTAR_ID_PRODUCTO.format(producto=producto))
    for row in result:
        b = True

    return b

def consultar_id_umedida(uMedida):
    b = False
    result = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=uMedida))
    for row in result:
        b = True
    return b

def consultar_id_marca(marca):
    b = False
    result = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=marca))
    for row in result:
        b = True
    return b

def Id_marca(marca):
    resultado = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=marca))
    for row in resultado:
        a = row.marca_id
    return a

def Id_tipo_producto(tProd):
    resultado = db.engine.execute(CONSULTAR_ID_TPRODUCTO.format(tProd=tProd))
    for row in resultado:
        a = row.tipo_producto_id
    return a

def producto_ide(producto,marca):
    resultado = db.engine.execute(PRODUCTO_IDE.format(producto=producto,marca=marca))
    for row in resultado:
        a = row.producto_id
    return a

def unidad_medida_ide(uMedida):
    resultado = db.engine.execute(UNIDADMEDIDA_IDE.format(uMedida=uMedida))
    for row in resultado:
        a = row.unidad_medida_id
    return a

def envase_ide(envase):
    print("vino envaseee {}".format(envase))
    resultado = db.engine.execute(ENVASE_IDE.format(envase=envase))
    for row in resultado:
        a = row.envase_id
    return a


def consulta_producto_pProducto(producto):
    resultado = db.engine.execute(PRODUCTOS_P_PRODUCTO.format(producto=producto))
    return parser_result(resultado)

def consulta_producto_pMarca(marca):
    resultado = db.engine.execute(PRODUCTOS_P_MARCA.format(marca=marca))
    return parser_result(resultado)

def consulta_producto_pUMedida(uMedida):
    resultado = db.engine.execute(PRODUCTOS_P_UMEDIDA.format(uMedida=uMedida))
    return parser_result(resultado)

def consulta_producto_pProductoMarca(producto,marca):
    resultado = db.engine.execute(PRODUCTOS_P_PRODUCTO_MARCA.format(producto=producto,\
    marca=marca))
    return parser_result(resultado)

def consulta_producto_pProductoUMedida(producto,uMedida):
    resultado = db.engine.execute(PRODUCTOS_P_PRODUCTO_UMEDIDA.format(producto=producto,\
    uMedida=uMedida))
    return parser_result(resultado)

def consulta_producto_pMarcaUMedida(marca,uMedida):
    resultado = db.engine.execute(PRODUCTOS_P_MARCA_UMEDIDA.format(marca=marca,\
    uMedida=uMedida))
    return parser_result(resultado)

def consulta_producto_pProductoMarcaUMedida(producto,marca,uMedida):
    resultado = db.engine.execute(PRODUCTOS_P_PRODUCTO_MARCA_UMEDIDA.format(producto=producto,\
    marca=marca,uMedida=uMedida))
    return parser_result(resultado)

def insert_new_producto(producto,marca,uMedida,tProd,envase):
    db.engine.execute(INSERT_T_PRODUCTO.format(producto=producto,marca=Id_marca(marca),tProd=Id_tipo_producto(tProd)))

    db.engine.execute(INSERT_T_PRODUCTO_ENVASE.format(producto=producto_ide(producto,marca),\
    envase=envase_ide(envase),uMedida=unidad_medida_ide(uMedida)))

    return True
