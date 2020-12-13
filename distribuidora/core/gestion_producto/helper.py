from distribuidora import db
from distribuidora.core.gestion_producto.query import *
from distribuidora.models.producto import Marca, TipoProducto, Envase, UnidadMedida, \
    Producto, ProductoEnvase
from distribuidora.models.precio import Lista_precio_producto
import csv
from datetime import datetime

#from distribuidora.core.gestion_stock.query import CONSULTA_STOCK1

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



def consulta_producto_pProductoMarcaUMedida(producto,marca,uMedida):

    resultado = db.engine.execute(PRODUCTOS_P_PRODUCTO_MARCA_UMEDIDA.format(producto=producto,\
    marca=marca,uMedida=uMedida))
    return parser_result(resultado)

def consult_producto(producto,marca,uMedida):
    result = None
    resultado = None
    r = []
    valor = None
    umed = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=uMedida))
    for row in umed:
        um = row.unidad_medida_id

    mar = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=marca))
    for row in mar:
        m = row.marca_id

    result = db.engine.execute(CONSULTA_ID_PRODUCTO_MARCA_UMEDIDA.format(producto=producto,marca=m,uMedida=um))
    for row in result:
        valor = row.producto_envase_id

    if valor == None:
        print("acaaaaaaaa")
        return -777

    resultado = db.engine.execute(CONSULTA_STOCK1.format(producto_envase_id=valor))
    resultado = parser_result(resultado)

    return resultado





def eli_producto(producto,marca,uMedida):
    val = None
    umed = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=uMedida))
    for row in umed:
        um = row.unidad_medida_id
    mar = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=marca))
    for row in mar:
        m = row.marca_id
    result = db.engine.execute(CONSULTAR_ID_PRODUCTO_MARCA_UMEDIDA.format(producto=producto,marca=m,uMedida=um))
    for row in result:
        val = row['producto_envase_id']
        print("valor {}".format(val))
        pro = row.producto_id
        print("pro {}".format(pro))
    #Borramos en la tabla producto_envase el producto
    db.engine.execute(ELIMINAR_PRODUCTO_ENVASE.format(producto=val))

    #Borramos en la tabla producto el producto
    db.engine.execute(ELIMINAR_PRODUCTO.format(producto=pro))





def consulta_producto_pProductoUMedida(producto,uMedida):
    resultado = db.engine.execute(PRODUCTOS_P_PRODUCTO_UMEDIDA.format(producto=producto,\
    uMedida=uMedida))
    return parser_result(resultado)

def consulta_producto_pMarcaUMedida(marca,uMedida):
    resultado = db.engine.execute(PRODUCTOS_P_MARCA_UMEDIDA.format(marca=marca,\
    uMedida=uMedida))
    return parser_result(resultado)





def insert_new_producto(producto,marca,uMedida,tProd,envase):
    db.engine.execute(INSERT_T_PRODUCTO.format(producto=producto,marca=Id_marca(marca),tProd=Id_tipo_producto(tProd)))

    db.engine.execute(INSERT_T_PRODUCTO_ENVASE.format(producto=producto_ide(producto,marca),\
    envase=envase_ide(envase),uMedida=unidad_medida_ide(uMedida)))

    return True


def modific_producto(pro,mar,um,env,tProd,pro1,mar1,um1):
    marca = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar1))
    umedida_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=um1))
    for row in marca:
        print("marca {}".format(row.marca_id))
        m1 = row.marca_id
    for row in umedida_id:
        print("um1 {}".format(row.unidad_medida_id))
        um1 = row.unidad_medida_id

    marca_id = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
    um_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=um))
    envase_id = db.engine.execute(ENVASE_IDE.format(envase=env))
    tp_id = db.engine.execute(TIPOPRODUCTOID.format(tp=tProd))
    for row in marca_id:
        m = row.marca_id
    for row in um_id:
        um = row.unidad_medida_id
    for row in envase_id:
        e = row.envase_id
    for row in tp_id:
        tp=row.tipo_producto_id

    result = db.engine.execute(CONSULTAR_ID_PRODUCTO_MARCA_UMEDIDA.format(producto=pro1,marca=m1,uMedida=um1))
    for row in result:
        pe_id = row['producto_envase_id']
        print("valor {}".format(pe_id))
        p = row.producto_id
        print("pro {}".format(p))

    db.engine.execute(UPDATEPRODUCTOENVASE.format(e=e,um=um,pe_id=pe_id))
    db.engine.execute(UPDATEPRODUCTO.format(pro=pro,m=m,tp=tp,p=p))



def importar_productos_from_file(path):
    print('IMPORTACION DE PRODUCTOS DESDE ARCHIVO POR PARTE DEL USUARIO OPERADOR')
    print(path)
    # hardcodeamos unas cuantas cosas
    productos_a_guardar = list()
    lista_precio = '1'
    f_desde = datetime.strptime('15/06/2020', "%d/%m/%Y")
    f_hasta = datetime.strptime('15/06/2021', "%d/%m/%Y")

    # recorremos el archivo ingresado
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #headers = csv.reader(csv_file)
        #headers = next(headers)
        print('HEADERS_ {}'.format(csv_reader.fieldnames))
        if csv_reader.fieldnames != ['PRODUCTO', 'UNIDAD', 'ENVASE', 'PRECIO', 'MARCA', 'TIPO_PRODUCTO', 'CANTIDAD']:
            return 'El archivo no tiene los campos necesarios'
            
        for row in csv_reader:
            # recupero los datos
            marca = Marca.query.filter_by(descripcion=row['MARCA']).first()
            unidad_medida = UnidadMedida.query.filter_by(descripcion=row['UNIDAD']).first()
            envase = Envase.query.filter_by(descripcion=row['ENVASE']).first()
            tipo_producto = TipoProducto.query.filter_by(descripcion=row['TIPO_PRODUCTO']).first()
            producto = Producto.query.filter_by(descripcion=row['PRODUCTO']).first()

            # si NO ingresan algun dato, corto el flujo y salgo
            if marca is None or unidad_medida is None or envase is None or tipo_producto is None or producto is None:
                return 'Hay datos que no existen en el Sistema.'
            precio = row['PRECIO'].replace(',', '.')
            precio = float(precio)

            # si el precio no es valido, corto el flujo y salgo
            if precio <= 0:
                return 'El valor del precio es incorrecto'
            
            # primero verifico si existe el producto
            pe = ProductoEnvase.query.filter_by(producto_id=producto.get_id(),\
                envase_id=envase.get_id(),\
                unidad_medida_id=unidad_medida.get_id()).first()

            # si no existe, lo creo
            if pe is None:
                pe = ProductoEnvase(producto_id=producto.get_id(),\
                    envase_id=envase.get_id(),\
                    unidad_medida_id=unidad_medida.get_id(),\
                    stock_real=row['CANTIDAD'])
                db.session.add(pe)
                db.session.commit()
            else:
                # si existe, actualizo su cantidad
                pe.stock_real = row['CANTIDAD']
                db.session.commit()

            pe = ProductoEnvase.query.filter_by(envase_id=envase.get_id(),\
                unidad_medida_id=unidad_medida.get_id(),\
                producto_id=producto.get_id()).first()
            
            # lo mismo para el precio, si no existe lo creo, caso contrario actualizo
            lista = Lista_precio_producto.query.filter_by(producto_envase_id=pe.get_id()).first()
            if lista is None:
                lista = Lista_precio_producto(producto_envase_id=pe.get_id(),\
                    precio_id=lista_precio,\
                    precio=row['PRECIO'],\
                    fecha_inicio=f_desde,\
                    fecha_fin=f_hasta)
                db.session.add(lista)
                db.session.commit()
            else:
                lista.precio =row['PRECIO']
                db.session.commit()

    return "Carga Exitosa"