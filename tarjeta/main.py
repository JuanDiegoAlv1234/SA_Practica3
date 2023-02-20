from flask import Flask, jsonify, request
from connection import *
import re

app = Flask(__name__)

##########################################################################
##########################################################################
##########################################################################
##########################################################################
@app.route("/tarjeta/agregar", methods=["GET", "POST"])
def tarjeta_agregar():
    errors = {}
    if request.method == "POST":
        # Body request
        required_fields = ('user_id', 'tarjeta_no', 'cvv', 'date')
        # Body request check
        for field_name in required_fields:
            if field_name not in request.json:
                errors = {
                    "error": f'{field_name} faltante.',
                    "desc": f'El campo {field_name} es obligatorio.'
                }
                break
        if len(errors) > 0:
            return jsonify(errors), 400
        ##########################################################################
        ##########################################################################
        # Request asign to variables
        user_id = str(request.json['user_id'])
        tarjeta_no =  str(request.json['tarjeta_no'])
        cvv =  str(request.json['cvv'])
        date =  str(request.json['date'])

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
        # Verify if tarjeta_no is numeric
        if re.match(r"^\d+$", tarjeta_no) is None:
            errors = {
                "error": 'Error en tarjeta_no.',
                "desc": 'tarjeta_no debe de ser tipo numerico'
            }
            return jsonify(errors), 406
        # Verify if tarjeta_no len 13 <= x <= 18
        if 13 > int(tarjeta_no) or int(tarjeta_no) > 18:
            errors = {
                "error": 'Error en tarjeta_no.',
                "desc": 'tarjeta_no debe de ser mayor o igual a 13 digitos o menor o igual a 18 digitos'
            }
            return jsonify(errors), 406
        # Verify if csv is numeric
        if re.match(r"^\d+$", cvv) is None:
            errors = {
                "error": 'Error en cvv.',
                "desc": 'cvv debe de ser tipo numerico'
            }
            return jsonify(errors), 406
        # Verify if cvv == 3 o 4
        if 3 != int(cvv) and int(cvv) != 4:
            errors = {
                "error": 'Error en cvv.',
                "desc": 'cvv debe de tener 3 o 4 digitos'
            }
            return jsonify(errors), 406
        # Body request check
        if not re.match(r"^(0?[1-9]|1[012])/\d{2}(\d{2})?$", date):
            errors.append({
                "error": 'Error en date.',
                "desc": 'date debe de ser tipo fecha con formato MM/YYYY o MM/YY'
            })
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
        if cardExists(user_id, tarjeta_no, cvv, date):
            errors = {
                "error": 'Error en tarjeta.',
                "desc": 'La tarjeta ingresada ya existe.'
            }
            return jsonify(errors), 409
        ##########################################################################
        ##########################################################################
        # Compra
        if not makeTarjeta(user_id, tarjeta_no, cvv, date):
            errors = {
                "error": 'Error desconocido.',
                "desc": 'Ha ocurrido un error inesperado, intente mas tarde.'
            }
            return jsonify(errors), 500

        return jsonify({
            "added": True
        })
    else:
        # GET not implemented
        errors = {
            "error": 'No implementado',
            "desc": 'El metodo que intentas acceder no ha sido implementado.'
        }
        return jsonify(errors), 501

##########################################################################
##########################################################################
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
