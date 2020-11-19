from distribuidora import db
from flask import flash
from distribuidora.core.gestion_stock.query import CONSULTA_STOCK, CONSULTAR_ID_MARCA, \
    CONSULTAR_ID_UMEDIDA, CONSULTAR_ID_PRODUCTO, INSERT_MOVIMIENTO_STOCK,UPDATE_STOCK_REAL, \
    BAJA_PRODUCTO, CONSULTAR_MOVIMIENTOS, CONSULTA_STOCK1
from distribuidora.core.gestion_pedido.query import LISTAR_DETALLE_PEDIDO, DETALLE_INFORMACION_FULL
#from distribuidora.core.gestion_pedido.helper import parser_result

def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def check(result):
    if result.rowcount == 1 :
        return True
    else:
        return False

def consulta_sotck(producto):
    """
    Realiza la consulta a la base para el stock del producto seleccionado.
    Nos devolverá la cantidad del producto seleccionado:
    """
    print("consultaStock {}".format(producto))
    result = db.engine.execute(CONSULTA_STOCK.format(producto_id=producto))
    resultado = []
    for row in result:
        a = row['cantidad']
        resultado.append(dict(row))

    if(a == None):
        resultado = []
        result = db.engine.execute(CONSULTA_STOCK1.format(producto_id=producto))
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
    result = db.engine.execute(CONSULTAR_MOVIMIENTOS.format(f_desde=desde,f_hasta=hasta))

    #print("ROWS {}".format(result.fetchall()))
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def actualizar_stock_real(pedido_id):
    """
    Dado un pedido, vamos a descontar las cantidades afectadas al pedido.
    En sqlite no tenemos stored procedure asi que vamos a improvisar.
    """

    detalle_pedido = db.engine.execute(DETALLE_INFORMACION_FULL.format(\
        pedido_id=pedido_id))
    detalle_pedido = parser_result(detalle_pedido)
    costo = 0
    for dp in detalle_pedido:
        print(dp, flush=True)
        stock_descontar = int(dp['cantidad']) - int(dp['stock_real'])
        if stock_descontar >= 0:
            costo += int(dp['cantidad']) * int(dp['precio'])
            print('stock suficiente, puedo descontar')
            detalle_pedido = db.engine.execute(BAJA_PRODUCTO.format(\
                producto_envase_id=pd['producto_envase_id'],\
                cantidad=dp['cantidad']))
    return costo
