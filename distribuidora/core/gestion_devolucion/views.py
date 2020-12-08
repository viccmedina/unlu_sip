from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db

devolucion = Blueprint('devoluciones', __name__, template_folder='templates')

@devolucion.route('/devolucion/index', methods=['GET'])
#@login_required
def index():
	return render_template('devolucion.html')