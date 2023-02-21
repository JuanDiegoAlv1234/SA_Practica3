from flask import Flask, jsonify, request
from connection import *
import re
##########################################################################
##########################################################################
app = Flask(__name__)
##########################################################################
##########################################################################
@app.route("/tarjeta/ver", methods=["GET", "POST"])
def tarjeta_ver():
    errors = {}
    if request.method == "POST":
        # Body request check
        if 'user_id' not in request.json:
            errors = {
                "error": 'user_id faltante.',
                "desc": 'El campo user_id es obligatorio.'
            }
        if len(errors) > 0:
            return jsonify(errors), 400
        ##########################################################################
        ##########################################################################
        # Request asign to variables
        user_id = str(request.json['user_id'])

        ##########################################################################
        ##########################################################################
        # Verify variable types
        # Verify if user_id is numeric
        if re.match(r"^\d+$", user_id) is None:
            errors = {
                "error": 'Error en user_id.',
                "desc": 'User_id debe de ser tipo numerico'
            }
            return jsonify(errors), 406
        ##########################################################################
        ##########################################################################
        # Verify
        # Verify user
        if not userExists(user_id):
            errors = {
                "error": 'Error de usuario.',
                "desc": 'El usuario no existe'
            }
            return jsonify(errors), 403
        # Verify card
        if not verifyUserHasCard(user_id):
            errors = {
                "error": 'Error en tarjeta.',
                "desc": 'No existen tarjetas a nombre de este usuario.'
            }
            return jsonify(errors), 404
        ##########################################################################
        ##########################################################################
        # Compra
        tarjetas = getTarjeta(user_id)
        if len(tarjetas) == 0:
            errors = {
                "error": 'Error desconocido.',
                "desc": 'Ha ocurrido un error inesperado, intente mas tarde.'
            }
            return jsonify(errors), 500

        return jsonify(tarjetas)
    else:
        # GET not implemented
        errors = {
            "error": 'No implementado',
            "desc": 'El metodo que intentas acceder no ha sido implementado.'
        }
        return jsonify(errors), 501
