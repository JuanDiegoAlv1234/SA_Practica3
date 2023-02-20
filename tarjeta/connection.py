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

def userExists(user_id):
    return True
def cardExists(user_id, tarjeta_no, cvv, date):
    return False
def verifyUserHasCard(user_id):
    return True

def makeTarjeta(user_id, tarjeta_no, cvv, date):
    return True
def getTarjeta(user_id):
    return { "cards":[
        {
            "tarjeta_id": 1,
            "tarjeta_numbers": 233333
        }, {
            "tarjeta_id": 3,
            "tarjeta_numbers": 434444444
        }
    ]}
