from distribuidora import db
from distribuidora.core.mensaje.query import *


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


def insert_nuevo_mensaje(data):
	result = db.engine.execute(INSERTAR_NUEVO_MENSAJE.format(\
        recipient_id=data['receptor'], \
        sender_id=data['emirsor'],\
        body=data['body']))
	return check(result)