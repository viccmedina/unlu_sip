from distribuidora import db, app
from flask import flash
from distribuidora.core.gestion_usuario.query import *


def updateContraseña(password_hash,username):
    db.engine.execute(UPDATE_USER.format(passw=password_hash,user=username))
