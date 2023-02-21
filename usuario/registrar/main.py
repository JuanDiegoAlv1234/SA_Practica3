from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import re
import bcrypt

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_database = os.getenv("DB_DATABASE")

def connect_db():
    # Configura tu conexión a la base de datos MySQL
    config = {
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'database': db_database
    }

    conn = mysql.connector.connect(**config)
    return conn


@app.route('/user/', methods=['POST'])
def crear_usuario():
    required_fields = ('firstname', 'lastname', 'email', 'username', 'password', 'password_confirm', 'phone',
                                                                                                     'birth_day')
    errors = []

    for field_name in required_fields:
        if field_name not in request.json:
            errors.append({
                "error": f'{field_name} is mandatory.',
                "desc": f'The field {field_name} is required to proceed.'
            })

    if len(errors) > 0:
        return jsonify(errors), 400

    firstname = request.json['firstname']
    lastname = request.json['firstname']
    email = request.json['email']
    username = request.json['username']
    birth_day = request.json['birth_day']
    password = request.json['password']
    password_confirm = request.json['password_confirm']
    phone = request.json['phone']

    # Validar formato de email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append({
            "error": f'Email invalid. ',
            "desc": f'Email format is not valid.'
        })

    # Validar formato de username
    if not re.match(r"^[a-zA-Z0-9]+$", username):
        errors.append({
            "error": f'username invalid. ',
            "desc": f'username can only include numbers and letters.'
        })

    if not re.match(r"^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(19|20)\d{2}$", birth_day):
        errors.append({
            "error": f'birthday invalid. ',
            "desc": f'Birth day should be in format dd/mm/yyyy'
        })

    if len(errors) > 0:
        return jsonify(errors), 400

    # Validar fecha de nacimiento
    birth_date = datetime.strptime(birth_day, '%d/%m/%Y').date()
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        errors.append({
            "error": f'User under age. ',
            "desc": f'You must be at least 18 years old to register. '
        })

    # Validar que las contraseñas coincidan
    if password != password_confirm:
        errors.append({
            "error": f'Password confirm do not match. ',
            "desc": f'Your passwords don\'t match.'
        })

    if len(errors) > 0:
        return jsonify(errors), 400

    # Insertar el usuario en la base de datos
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query = "INSERT INTO Users (firstname, lastname, email, username, birth_day, encrypted_password, phone) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(query, (firstname, lastname, email, username, birth_day, encrypted_password, phone))


    return '', 201


if __name__ == '__main__':
    app.run()
