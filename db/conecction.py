from dotenv import load_dotenv
import os
import mysql.connector

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def conectar_bd():
    mydb = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        port=os.getenv("PORT")
    )
    return mydb