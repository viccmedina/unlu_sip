CONSULTAR_NRO_CUENTA_CORRIENTE = """
	SELECT cuenta_corriente_id FROM cuenta_corriente
	WHERE persona_id=('{nro_cliente}')
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE = """
	SELECT * FROM movimiento_cta_corriente
	WHERE ts_created>=DATETIME('{fecha_desde}') and
		ts_created<=('{fecha_hasta}') and cta_corriente=('{nro_cliente}')
	"""

SELECT_TIPO_MOVIMIENTOS = """
	SELECT descripcion FROM tipo_movimiento_cta_corriente
	"""

SELECT_ID_TIPO_MOVIMIENTO = """
	SELECT id FROM tipo_movimiento_cta_corriente
	WHERE descripcion=('{tipo_movimiento}')
"""

INSERT_MOV_CTA_CORRIENTE = """ INSERT INTO movimiento_cta_corriente
(cta_corriente, tipo_movimiento_cta_corriente, usuario, saldo, descripcion)
VALUES ('{n_cta}', '{t_mov}', '{user}', '{monto}', '{descripcion}') """

# primero sumo todas las deudas(id= 2) y desp le resto los pagos y reembolsos (id= 1 y3 )

CONSULTAR_SALDO = """SELECT DISTINCT mcc.cta_corriente AS cta_corriente, p.email AS email, p.nombre as nombre,
	((SELECT sum(mov.saldo) FROM movimiento_cta_corriente mov WHERE cta_corriente = {nro_cta}
	and tipo_movimiento_cta_corriente = 2)
	-
	(SELECT sum(mov.saldo * -1) FROM movimiento_cta_corriente mov  WHERE cta_corriente = {nro_cta}
	and tipo_movimiento_cta_corriente = 1 or tipo_movimiento_cta_corriente = 3 )) AS saldo
	FROM movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id
	INNER JOIN persona p ON cc.persona_id = p.persona_id WHERE mcc.cta_corriente = {nro_cta}

"""

"""
SELECT DISTINCT mcc.cta_corriente AS cta_corriente, p.email AS user,
((SELECT sum(mov1.saldo) FROM movimiento_cta_corriente mov1 WHERE mov1.cta_corriente = 1 and
mov1.tipo_movimiento_cta_corriente = 2)
-
(SELECT sum(mov.saldo * -1) FROM movimiento_cta_corriente mov
WHERE mov.cta_corriente = 1 and mov.tipo_movimiento_cta_corriente = 1 or mov.tipo_movimiento_cta_corriente = 3 )) AS saldo
FROM movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id
INNER JOIN persona p ON cc.persona_id = p.persona_id WHERE mcc.cta_corriente = 1 ;


1|cliente@prueba.com.ar|-1501.0
"""
