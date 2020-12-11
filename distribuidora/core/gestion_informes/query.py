
CONSULTAR_USUARIO = """
SELECT u.id FROM usuario u;
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE = """
	SELECT cc.cuenta_corriente_id AS cta_corriente,p.nombre AS nombre,p.email AS email,((SELECT sum(saldo) FROM movimiento_cta_corriente mccc WHERE
    mccc.usuario = {user}) - (SELECT sum(monto) FROM comprobante_pago cpp INNER JOIN pedido ped WHERE ped.usuario_id = {user})) AS saldo FROM
    movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id INNER JOIN persona p
    ON cc.persona_id = p.persona_id INNER JOIN pedido pe ON pe.usuario_id = mcc.usuario WHERE mcc.usuario = {user}

	"""
