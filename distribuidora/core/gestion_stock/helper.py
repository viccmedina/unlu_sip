from distribuidora import db, app
from flask import flash
from distribuidora.core.gestion_stock.query import *
from distribuidora.core.gestion_pedido.query import LISTAR_DETALLE_PEDIDO, DETALLE_INFORMACION_FULL
from distribuidora.models.producto import ProductoEnvase
from distribuidora.models.stock import Movimiento_Stock
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

def consulta_sotck1(producto):
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



def consulta_sotck(pro,mar,umed):
    """
    Dado un producto su marca y unidad de medida obtendremos el id.
    """
    valor = None
    marcaID = None
    a = None
    umedidaID = None
    result = None
    r = []
    resultado = None
    #buscar por producto solo
    if mar == '' and umed == '' :
        result = db.engine.execute(CONSULTAR_ID_PRODUCTO.format(producto=pro))
        for row in result:
            a = row['producto_envase_id']
            if a is None:
                valor = -666
            else:
                resultado = db.engine.execute(CONSULTA_STOCK_POR_PRODUCTO.format(producto_id=row['producto_envase_id']))
                for rows in resultado:
                    r.append(dict(rows))
    else:
        #Buscar por marca sola
        if pro == '' and umed == '' :
            result = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
            for row in result:
                a = row['marca_id']
                if a is None:
                    valor=-999
                else:
                    resultado = db.engine.execute(CONSULTA_STOCK_POR_MARCA.format(marca=row['marca_id']))
                    for rows in resultado:
                        r.append(dict(rows))
        else:
            #Buscar por unidad de medida solo
            if pro =='' and mar == '':
                result = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=umed))
                for row in result:
                    a = row['unidad_medida_id']
                    if a is None:
                        valor= -888
                    else:
                        resultado = db.engine.execute(CONSULTA_STOCK_POR_UMEDIDA.format(uMedida=row['unidad_medida_id']))
                        for rows in resultado:
                            r.append(dict(rows))
            else:
                #Buscar por producto-marca
                if umed == '':
                    mar_id = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
                    for row in mar_id:
                        marcaID = row['marca_id']
                        print("marcaaasss: ", marcaID)
                    if marcaID is None:
                        valor = -999
                    else:
                        result = db.engine.execute(CONSULTA_ID_POR_PRODUCTO_MARCA.format(producto=pro,marca=marcaID))
                        for row in result:
                            a = row['producto_envase_id']
                            if a is None:
                                valor= -666
                            else:
                                resultado = db.engine.execute(CONSULTA_STOCK_POR_PRODUCTO_MARCA.format(\
                                producto=row['producto_envase_id']))
                                for rows in resultado:
                                    r.append(dict(rows))
                else:
                    #Buscar por producto-unidad de medida
                    if mar == '' :
                        umed_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=umed))
                        for row in umed_id:
                            umedidaID = row['unidad_medida_id']
                            print("unidaddddd: ", umedidaID)
                        if umedidaID is None:
                            valor = -888
                        else:
                            result = db.engine.execute(CONSULTA_ID_POR_PRODUCTO_UMEDIDA.format(producto=pro,uMedida=umedidaID))
                            for row in result:
                                a = row['producto_envase_id']
                                if a is None:
                                    valor= -666
                                else:
                                    resultado = db.engine.execute(CONSULTA_STOCK_POR_PRODUCTO_UMEDIDA.format(\
                                    producto=row['producto_envase_id']))
                                    for rows in resultado:
                                        r.append(dict(rows))
                    else:
                        #Buscar por marca-unidad de medida
                        if pro == '':
                            umed_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=umed))
                            for row in umed_id:
                                umedidaID = row['unidad_medida_id']
                                print("unid: ", umedidaID)
                            if umedidaID is None:
                                valor = -888
                            else:
                                mar_id = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
                                for row in mar_id:
                                    marcaID = row['marca_id']
                                    print("marcapapa: ", marcaID)
                                if marcaID is None:
                                    valor = -999
                                else:
                                    result = db.engine.execute(CONSULTA_ID_POR_MARCA_UMEDIDA.format(marca=marcaID,uMedida=umedidaID))
                                    for row in result:
                                        a = row['producto_envase_id']
                                        if a is None:
                                            valor = -555
                                        else:
                                            resultado = db.engine.execute(CONSULTA_STOCK_POR_MARCA_UMEDIDA.format(\
                                            producto=row['producto_envase_id']))
                                            for rows in resultado:
                                                r.append(dict(rows))
                        else:
                            #Buscar por producto-marca-unidad de medida
                            umed_id = db.engine.execute(CONSULTAR_ID_UMEDIDA.format(uMedida=umed))
                            for row in umed_id:
                                umedidaID = row['unidad_medida_id']
                                print("unidaddddd: ", umedidaID)

                            if umedidaID is None:
                                valor = -888
                            else:
                                mar_id = db.engine.execute(CONSULTAR_ID_MARCA.format(marca=mar))
                                for row in mar_id:
                                    marcaID = row['marca_id']
                                    print("marcaaasss: ", marcaID)
                                if marcaID is None:
                                    valor = -999
                                else:
                                    result = db.engine.execute(CONSULTA_ID_PRODUCTO_MARCA_UMEDIDA.format(\
                                    marca=marcaID,uMedida=umedidaID,producto=pro))
                                    for row in result:
                                        valor = row['producto_envase_id']
                                        print("producto-envase: ", valor)

                                    if valor is None:
                                        return -777
                                    else:
                                        resultado = db.engine.execute(CONSULTA_STOCK1.format(\
                                        producto_envase_id=row['producto_envase_id']))
                                        for rows in resultado:
                                            r.append(dict(rows))
    if valor is None or valor == -999 or valor == -888 or valor == -777 or valor == -666 or valor == -555:
        print("valor es sssss{}".format(valor) )
        return valor
    else:
        return r





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
    print('detalle_pedido ---- {}'.format(detalle_pedido), flush=True)
    costo = 0
    save = list()
    for dp in detalle_pedido:
        stock_descontar = int(dp['stock_real'])- int(dp['cantidad'])
        print('stock a descontar ---> {}'.format(stock_descontar), flush=True)
        if stock_descontar >= 0:
            costo += float(dp['cantidad'].replace(',','.')) * float(dp['precio'].replace(',','.'))
            #detalle_pedido = db.engine.execute(UPDATE_NUEVO_PEDIDO_STOCK_REAL.format(producto_envase_id=dp['producto_envase_id'], stock_real=stock_descontar))
            pe = ProductoEnvase.query.get(dp['producto_envase_id'])
            print(pe, flush=True)
            pe.stock_real = stock_descontar
            save.append(pe)
    db.session.add_all(save)
    db.session.commit()
    return costo

def agregar_historial_movimientos_stock(pedido_id, operador_id, tipo_movimiento, tipo='PEDIDO'):
    print('AGREGAMOS STOCK AL HISTORIAL DE MOVIMIENTOS')
    add_historial = list()
    detalle_pedido = db.engine.execute(DETALLE_INFORMACION_FULL.format(\
        pedido_id=pedido_id))
    detalle_pedido = parser_result(detalle_pedido)
    movimiento = db.engine.execute(SELECT_TIPO_MOVIMIENTO_STOCK.format(descripcion=tipo_movimiento))
    movimiento = parser_result(movimiento)
    movimiento_id = movimiento[0]['tipo_movimiento_stock_id']
    for d in detalle_pedido:
        if tipo == 'PEDIDO':
            nuevo_movimiento_stock = Movimiento_Stock(detalle_pedido_id=d['detalle_id'],\
                tipo_movimiento_stock_id=movimiento_id,\
                usuario_id=operador_id,\
                producto_envase_id=d['producto_envase_id'],\
                descripcion='MOVIMIENTO POR PEDIDO',\
                cantidad=d['cantidad'])
            add_historial.append(nuevo_movimiento_stock)
    db.session.add_all(add_historial)
    db.session.commit()
    print('>'*100)

def get_movimientos_by_fechas(desde, hasta):
    result = db.engine.execute(SELECT_MOVIMIENTOS_BY_FECHA.format(\
        fecha_desde=desde, fecha_hasta=hasta))
    result = parser_result(result)
    return result