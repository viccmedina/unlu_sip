from distribuidora import db
from distribuidora.core.gestion_cta_corriente.query import SELECT_TIPO_MOVIMIENTOS

def get_tipos_movimientos():
    """
    Realiza la consulta a la base para obtener los tipos de movimientos.
    Nos devolverá una lista del tipo:
    ['Deuda', 'Pago', 'Reembolso']
    """
    result = db.engine.execute(SELECT_TIPO_MOVIMIENTOS)
    resp = []
    for row in result:
        resp.append(row)
    return resp
