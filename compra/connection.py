from dotenv import load_dotenv
from enum import Enum
import os

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_database = os.getenv("DB_DATABASE")

def connect_db():
    config = {
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'database': db_database
    }
    conn = mysql.connector.connect(**config)
    return conn

class AsientoStatus(Enum):
    NoExiste = 1
    Ocupado = 2
    Disponible = 3

def userExists(user_id):
    return True
def movieExists(funcion_pelicula_id):
    return True
def verifyCard(user_id, tarjeta_id):
    return True
def salaExists(sala_id):
    return True
def salaCorrect(funcion_pelicula_id, sala_id):
    return True
def verifyAsientos(funcion_pelicula_id, sala_id, tickets):
    asientoStatus = AsientoStatus.Disponible
    return [asientoStatus, 0]
def verifyMembresia(user_id):
    return False

def makeCompra(user_id, funcion_pelicula_id, tickets, tarjeta_id):
    return True
def makeMembresia(user_id, tickets):
    return True
def makeMembresiaCancelar(user_id):
    return True
