from distribuidora import db
from flask import flash
from distribuidora.core.gestion_stock.query import CONSULTA_STOCK, CONSULTAR_ID_MARCA, \
CONSULTAR_ID_UMEDIDA, CONSULTAR_ID_PRODUCTO, INSERT_MOVIMIENTO_STOCK,UPDATE_STOCK_REAL, \
BAJA_PRODUCTO, CONSULTAR_MOVIMIENTOS

def consulta_sotck(producto):
    """
    Realiza la consulta a la base para el stock del producto seleccionado.
    Nos devolverá la cantidad del producto seleccionado:
    """
    print("consultaStock {}".format(producto))
    result = db.engine.execute(CONSULTA_STOCK.format(producto_id=producto))
    #entrada = db.engine.execute(CONSULTA_ENTRADA_STOCK.format(producto_id=producto))
    #salida = db.engine.execute(CONSULTA_SALIDA_STOCK.format(producto_id=producto))
    resultado = []
    for row in result:
        resultado.append(dict(row))
    print(resultado)
    return resultado


def get_id_producto(pro,mar,umed):
    """
    Dado un producto su marca y unidad de medida obtendremos el id.
    """
    print("el producto es este " + pro)
    valor = None
    marcaID = None
    umedidaID = None
    mar_id = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
    for row in mar_id:
        marcaID = row['marca_id']
        print("marcaaasss: ", marcaID)

    if marcaID is None:
        valor = -999
    else:
        umed_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=umed))
        for row in umed_id:
            umedidaID = row['unidad_medida_id']
            print("unidaddddd: ", umedidaID)

        if umedidaID is None:
            valor = -888
        else:
            result = db.engine.execute(CONSULTAR_ID_PRODUCTO.format(marca=marcaID,uMedida=umedidaID,producto=pro))
            for row in result:
                valor = row['producto_envase_id']
                print("producto-envase: ", valor)

            if valor is None:
                return -777
            else:
                return valor
        return valor
    return valor




def agregar_stock(usuario,producto,cantidad,desc):
    """
    Esta funcion agregara un nueva tupla en la tabla movimiento_stock
    """


    descripcion = "Carga de {}".format(desc)
    print("descripcion: "+ descripcion)
    db.engine.execute(INSERT_MOVIMIENTO_STOCK.format(tipo_movimiento=1,usuario_id=usuario,producto_envase_id=producto,cantidad=cantidad,descripcion=descripcion))
    db.engine.execute(UPDATE_STOCK_REAL.format(producto_envase_id=producto,cantidad=cantidad))
    return "ok"



def salida(usuario,producto,cantidad,desc):
    """ Esta funcion insetara una tupla en la tabla movimientos, reflejando
    la baja de un producto y se descontara del stock real en la tabla proudcto_envase
    ojo es baja por rotura o vto, no es devolucion
    """
    descripcion = "Se quita {} por mal estado".format(desc)
    db.engine.execute(INSERT_MOVIMIENTO_STOCK.format(tipo_movimiento=2,usuario_id=usuario,producto_envase_id=producto,cantidad=cantidad,descripcion=descripcion))
    db.engine.execute(BAJA_PRODUCTO.format(producto_envase_id=producto,cantidad=cantidad))

def consultaMovimientosExportar(desde,hasta):
    print("fecha_desde {}".format(desde) )
    print("fecha_hasta {}".format(hasta) )
    #result = db.engine.execute(CONSULTAR_MOVIMIENTOS.format(f_desde=desde,f_hasta=hasta))
    result = db.engine.execute("SELECT p.descripcion as descripcion_p, m.descripcion as descripcion_m, um.descripcion, u.username, mov.ts_created as fecha, mov.cantidad FROM ((((movimiento_stock mov INNER JOIN producto_envase pe on mov.producto_envase_id=pe.producto_envase_id) INNER JOIN producto p on p.producto_id= pe.producto_id) INNER JOIN marca m on p.marca_id= m.marca_id) INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id INNER JOIN usuario u on u.id=mov.usuario_id) WHERE mov.ts_created >= DATETIME('2020-11-10') and mov.ts_created <= ('2020-11-18');")

    #print("ROWS {}".format(result.fetchall()))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp
