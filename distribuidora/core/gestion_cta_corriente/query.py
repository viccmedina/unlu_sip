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
(cta_corriente,tipo_movimiento_cta_corriente,usuario,saldo,descripcion)
VALUES ( {n_cta},{t_mov},{user},{monto},'{descripcion}' ) """

CONSULTAR_SALDO = """
	SELECT sum(mov.monto) FROM movimiento_cta_corriente WHERE cuenta_corriente_id = {nro_cta}
	and tipo_movimiento_cta_corriente = 2
"""
