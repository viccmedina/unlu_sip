from distribuidora import db
from distribuidora.core.gestion_lista_precio.query import *
from distribuidora.models.precio import Lista_precio_producto, Lista_precio
from distribuidora.models.producto import ProductoEnvase
import csv
import datetime

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def importar_lista_precios_from_file(path):
    print('@'*100)
    print('IMPORTACION DE LISTA DE PRECIO DESDE ARCHIVO POR PARTE DEL USUARIO OPERADOR')
    print(path)
    formato='%d-%m-%Y'

    # recorremos el archivo ingresado
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #headers = csv.reader(csv_file)
        #headers = next(headers)
        print('HEADERS_ {}'.format(csv_reader.fieldnames))
        if csv_reader.fieldnames != ['FECHA_DESDE', 'FECHA_HASTA', 'PRODUCTO_ENVASE', 'PRECIO', 'LISTA_PRECIO']:
            return 'El archivo no tiene los campos necesarios'

        for row in csv_reader:
            # debemos verificar e id de producto_envase
            producto_envase = ProductoEnvase.query.filter_by(producto_envase_id=row['PRODUCTO_ENVASE']).first()
            lista_precio = Lista_precio.query.filter_by(precio_id=row['LISTA_PRECIO'])
            precio = float(row['PRECIO'].replace(',','.'))
            if producto_envase is None:
                return 'El campo "PRODUCTO_ENVASE" : {} no existe en el sistema'.format(row['PRODUCTO_ENVASE'])

            elif precio <= 0:
                return 'El campo "PRECIO" : {} no es válido'.format(row['PRECIO'])
            elif lista_precio is None:
                return 'La lista de precio #{} no es válida'

            existe = Lista_precio_producto.query.filter_by(producto_envase_id=row['PRODUCTO_ENVASE'],\
                precio_id=row['LISTA_PRECIO']).first()

            print(existe)

            if  existe is None:

                lpp = Lista_precio_producto(producto_envase_id=row['PRODUCTO_ENVASE'],\
                    precio_id=row['LISTA_PRECIO'],\
                    fecha_inicio=datetime.datetime.strptime(row['FECHA_DESDE'].replace('/','-'), formato).date(),\
                    fecha_fin=datetime.datetime.strptime(row['FECHA_HASTA'].replace('/','-'), formato).date(),\
                    precio=precio)
                db.session.add(lpp)
                db.session.commit()
            else:
                print('EL PRODUCTO EXISTE')
                existe.precio = precio
                db.session.commit()

    return "Carga Exitosa"


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
    #db.engine.execute(AGREGAR_PRECIO.format(fecha=fecha))
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
