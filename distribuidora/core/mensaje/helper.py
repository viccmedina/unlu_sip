from distribuidora import db
from distribuidora.core.mensaje.query import *


def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp

def operadores():
    resp = []
    resultado = db.engine.execute(SELECT_OPERADORES)
    for row in resultado:
        resp.append(row.name)
    return resp

def id_operador(operador):
    resp = []
    resultado = db.engine.execute(SELECT_ID_OPERADOR.format(oper=operador))
    for row in resultado:
        print("Row {}".format(row.id))
        resp.append(row.id)
    return resp

def check(result):
    if result.rowcount == 1 :
        return True
    else:
        return False

def insert_nuevo_mensaje(data,id_oper):
	result = db.engine.execute(INSERTAR_NUEVO_MENSAJE.format(\
        recipient_id=id_oper, \
        sender_id=data['emisor'],\
        body=data['body']))
	return check(result)

def get_mensajes(usuario_id):
	enviados = db.engine.execute(SELECT_TODOS_MIS_MENSAJES_ENVIADOS.format(\
		usuario_id=usuario_id))
	enviados = parser_result(enviados)
	print(enviados, flush=True)

	recibidos = db.engine.execute(SELECT_TODOS_MIS_MENSAJES_RECIBIDOS.format(\
		usuario_id=usuario_id))
	print('x'*100, flush=True)
	recibidos = parser_result(recibidos)
	print(recibidos, flush=True)
	sin_leer = db.engine.execute(SELECT_MENSAJES_SIN_LEER.format(\
		usuario_id=usuario_id))
	print('x'*100, flush=True)
	sin_leer = parser_result(sin_leer)
	print(sin_leer, flush=True)
	print(type(sin_leer), flush=True)

	datos = {"recibidos": recibidos, \
		"enviados": enviados, \
		"sin_leer": {"msjs":sin_leer, "cantidad": len(sin_leer)}
		}
	print('x'*100, flush=True)
	print(datos, flush=True)

	return datos

def get_cantidad_msj_sin_leer(usuario_id):
	sin_leer = db.engine.execute(CANTIDAD_MSJS_SIN_LEER.format(\
		usuario_id=usuario_id))
	return parser_result(sin_leer)

def update_read_mensaje(mensaje_id):
	result = db.engine.execute(LEER_MENSAJE.format(\
		mensaje_id=mensaje_id))
	return check(result)
