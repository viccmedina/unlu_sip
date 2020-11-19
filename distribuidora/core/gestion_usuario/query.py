JOIN_PERSONA_USER = """ SELECT p.persona_id FROM persona AS p
    INNER JOIN usuario as U ON u.persona_id=p.persona_id
    WHERE u.id = '{usuario_id}'
    """
