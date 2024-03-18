from dotenv import load_dotenv
import os
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a MySQL
USERNAME = os.getenv("DB_USER")
PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_DATABASE")

# Crear una instancia de la clase Base
Base = declarative_base()

# Crear una conexión a la base de datos MySQL
engine = create_engine(f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}', pool_pre_ping=True)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)