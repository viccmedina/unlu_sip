from distribuidora import db
from distribuidora.core.gestion_stock.query import CONSULTA_STOCK, CONSULTA_ENTRADA_STOCK , CONSULTA_SALIDA_STOCK, CONSULTAR_ID_MARCA, CONSULTAR_ID_UMEDIDA, CONSULTAR_ID_PRODUCTO

def consulta_sotck(producto):
    """
    Realiza la consulta a la base para el stock del producto seleccionado.
    Nos devolverá la cantidad del producto seleccionado:
    """
    print("consultaStock {}".format(producto))
    #result = db.engine.execute(CONSULTA_STOCK.format(producto_id=producto))
    entrada = db.engine.execute(CONSULTA_ENTRADA_STOCK.format(producto_id=producto))
    salida = db.engine.execute(CONSULTA_SALIDA_STOCK.format(producto_id=producto))

    for row in entrada:
        e = row[0]
    for row in salida:
        s = row[0]
    if e is None:
        return 0 - s
    else:
        if s is None :
            return e
        else :
            return e - s


def get_id_producto(pro,mar,umed):
    """
    Dado un producto su marca y unidad de medida obtendremos el id.
    """
    print("el producto es este " + pro)
    valor = None
    mar_id = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
    for row in mar_id:
        marcaID = row['marca_id']
        print("marcaaasss: ", marcaID)
    umed_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=umed))
    for row in umed_id:
        umedidaID = row['unidad_medida_id']
        print("unidaddddd: ", umedidaID)


    result = db.engine.execute(CONSULTAR_ID_PRODUCTO.format(marca=marcaID,uMedida=umedidaID,producto=pro))

    for row in result:
        valor = row['producto_id']
        print("producto: ", valor)

    if valor is None:
        return -100
    else:
        return valor
