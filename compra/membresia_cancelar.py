from flask import Flask, jsonify, request
from connection import *
import re
##########################################################################
##########################################################################
app = Flask(__name__)
##########################################################################
##########################################################################
@app.route("/compra/membresia_cancelar", methods=["GET", "POST"])
def compra_membresia_cancelar():
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
        # Verify membresia
        if not verifyMembresia(user_id):
            errors = {
                "error": 'Error de compra.',
                "desc": 'El usuario ya posee la membresia.'
            }
            return jsonify(errors), 409
        
        ##########################################################################
        ##########################################################################
        # Compra
        if not makeMembresiaCancelar(user_id):
            errors = {
                "error": 'Error desconocido.',
                "desc": 'Ha ocurrido un error inesperado, intente mas tarde.'
            }
            return jsonify(errors), 500

        return jsonify({
            "signed": True
        })
    else:
        # GET not implemented
        errors = {
            "error": 'No implementado',
            "desc": 'El metodo que intentas acceder no ha sido implementado.'
        }
        return jsonify(errors), 501