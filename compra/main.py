from flask import Flask, jsonify, request
from connection import *
import re

app = Flask(__name__)

##########################################################################
##########################################################################
##########################################################################
##########################################################################
@app.route("/compra/boleto", methods=["GET", "POST"])
def compra_boleto():
    errors = {}
    if request.method == "POST":
        # Body request
        required_fields = ('user_id', 'funcion_pelicula_id', 'tarjeta_id', 'sala_id', 'tickets')
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
        funcion_pelicula_id =  str(request.json['funcion_pelicula_id'])
        tarjeta_id =  str(request.json['tarjeta_id'])
        sala_id =  str(request.json['sala_id'])
        tickets =  str(request.json['tickets'])

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
        # Verify if funcion_pelicula_id is numeric
        if re.match(r"^\d+$", funcion_pelicula_id) is None:
            errors = {
                "error": 'Error en funcion_pelicula_id.',
                "desc": 'funcion_pelicula_id debe de ser tipo numerico'
            }
            return jsonify(errors), 406
        # Verify if tarjeta_id is numeric
        if re.match(r"^\d+$", tarjeta_id) is None:
            errors = {
                "error": 'Error en tarjeta_id.',
                "desc": 'tarjeta_id debe de ser tipo numerico'
            }
            return jsonify(errors), 406
        # Verify if sala_id is numeric
        if re.match(r"^\d+$", sala_id) is None:
            errors = {
                "error": 'Error en sala_id.',
                "desc": 'sala_id debe de ser tipo numerico'
            }
            return jsonify(errors), 406
        # Body request check
        if ('asiento_id') not in tickets:
            errors = {
                "error": 'asiento_id faltante.',
                "desc": 'El campo asiento_id es obligatorio en tickets.'
            }
        if len(errors) > 0:
            return jsonify(errors), 400
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
        # Verify movie
        if not movieExists(funcion_pelicula_id):
            errors = {
                "error": 'Error en funcion.',
                "desc": 'La funcion que intentas comprar no existe.'
            }
            return jsonify(errors), 404
        # Verify card
        if not verifyCard(user_id, tarjeta_id):
            errors = {
                "error": 'Error en tarjeta.',
                "desc": 'Los datos de la tarjeta ingresada no existe.'
            }
            return jsonify(errors), 404
        # Verify sala :v
        if not salaExists(sala_id):
            errors = {
                "error": 'Error en sala.',
                "desc": 'Los sala no existe.'
            }
            return jsonify(errors), 404
        # Verify sala and movie 
        if not salaCorrect(funcion_pelicula_id, sala_id):
            errors = {
                "error": 'Error en sala.',
                "desc": 'Los sala escogida no esta asignada a la pelicula a ver.'
            }
            return jsonify(errors), 409
        # Verify asientos
        asientoStatus_arr = verifyAsientos(funcion_pelicula_id, sala_id, tickets)
        if asientoStatus_arr[0] != AsientoStatus.Disponible:
            if asientoStatus_arr[0] == AsientoStatus.NoExiste:
                errors = {
                    "error": 'Error en sala.',
                    "desc": f'El asiento {asientoStatus_arr[1]} no existe.'
                }
                return jsonify(errors), 404
            else:
                errors = {
                    "error": 'Error en sala.',
                    "desc": f'El asiento {asientoStatus_arr[1]} está ocupado.'
                }
                return jsonify(errors), 409
        ##########################################################################
        ##########################################################################
        # Compra
        if not makeCompra(user_id, funcion_pelicula_id, tickets, tarjeta_id):
            errors = {
                "error": 'Error desconocido.',
                "desc": 'Ha ocurrido un error inesperado, intente mas tarde.'
            }
            return jsonify(errors), 500

        return jsonify({
            "bought": True
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
@app.route("/compra/membresia_comprar", methods=["GET", "POST"])
def compra_membresia():
    errors = {}
    if request.method == "POST":
        # Body request
        required_fields = ('user_id', 'tarjeta_id')
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
        tarjeta_id =  str(request.json['tarjeta_id'])

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
        # Verify if tarjeta_id is numeric
        if re.match(r"^\d+$", tarjeta_id) is None:
            errors = {
                "error": 'Error en tarjeta_id.',
                "desc": 'tarjeta_id debe de ser tipo numerico'
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
        if not verifyCard(user_id, tarjeta_id):
            errors = {
                "error": 'Error en tarjeta.',
                "desc": 'Los datos de la tarjeta ingresada no existe.'
            }
            return jsonify(errors), 404
        # Verify membresia
        if verifyMembresia(user_id):
            errors = {
                "error": 'Error de compra.',
                "desc": 'El usuario ya posee la membresia.'
            }
            return jsonify(errors), 409
        
        ##########################################################################
        ##########################################################################
        # Compra
        if not makeMembresia(user_id, tarjeta_id):
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

##########################################################################
##########################################################################
##########################################################################
##########################################################################
@app.route("/compra/membresia_cancelar", methods=["GET", "POST"])
def compra_membresia_cancelar():
    errors = {}
    if request.method == "POST":
        # Body request
        required_fields = ('user_id')
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