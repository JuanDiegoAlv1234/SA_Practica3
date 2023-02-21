from flask import Flask, jsonify, request
import re

app = Flask(__name__)


# * Servicio de salas de cine
@app.route("/salas", methods=["GET"])
def ver_salas():

    # Arreglo de salas de cine
    salas = [
        {
            "id_sala": 1,
            "capacidad": 50
        },
        {
            "id_sala": 1,
            "capacidad": 50
        }
    ]

    parametro = int(request.args.get('id_sucursal'))
    req_mesg = "El listado de salas de la sucursal {} fue obtenida con exito".format(
        parametro)

    # Validación de codigo de sucursal

    return jsonify({
        "type": "success",
        "msg": req_mesg,
        "id_sucursal": parametro,
        "salas": salas
    })


# * Servicio para crear nuevas salas
@app.route("/salas/ingresar", methods=["POST"])
def ingresar_sala():

    required_fields = ('id_sucursal', 'nombre_sala', 'capacidad')

    # Lista de errores
    errors = []

    for field_name in required_fields:

        if field_name not in request.json:

            errors.append({
                "error": f'{field_name} is mandatory.',
                "desc": f'The field {field_name} is required to proceed.'
            })

    if len(errors) > 0:

        return jsonify(errors), 400

    # * Body request
    id_sucursal = int(request.json['id_sucursal'])
    nombre_sala = request.json['nombre_sala']
    capacidad = int(request.json['capacidad'])

    # * Validar id_sucursal
    if id_sucursal < 0:
        errors.append({
            "error": f'Sucursal de cine no valida',
            "desc": f"Tu numero de sucursal debe ser mayor a 0"
        })

    # * Validar nombre_sala

    # * Validar capacidad
    if id_sucursal < 0:
        errors.append({
            "error": f'Capacidad de sala valida',
            "desc": f"Tu capacidad debe ser mayor a 0"
        })

    # req_mesg = "El listado de salas de la sucursal {} fue obtenida con exito".format(parametro)

    # Validación de codigo de sucursal

    return jsonify({
        "type": "success",
        "msg": "La sala ha sido creada de forma exitosa"
    })
