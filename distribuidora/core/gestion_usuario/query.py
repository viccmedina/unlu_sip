JOIN_PERSONA_USER = """ SELECT p.persona_id FROM persona AS p
    INNER JOIN usuario as U ON u.persona_id=p.persona_id
    WHERE u.id = '{usuario_id}'
    """
VALIDAR_USER = """
SELECT u.username FROM usuario u WHERE u.id = {uid}
"""
UPDATE_USER = """
UPDATE usuario SET password_hash = '{passw}' where username = '{user}';
"""
