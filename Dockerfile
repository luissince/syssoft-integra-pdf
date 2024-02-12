# Utiliza la imagen base xanderls/python3.12-wkhtmltopdf:1.1.0
FROM xanderls/python3.12-wkhtmltopdf:1.1.0

# Copia el contenido del directorio actual al directorio /app en el contenedor
COPY . /app

# Crea un entorno virtual llamado myenv
RUN python3.12 -m venv myenv

# Copia el script start.sh al directorio raíz del contenedor
COPY start.sh .

# Concede permisos de ejecución al script start.sh
RUN chmod +x start.sh

# Activa el entorno virtual y luego instala las dependencias del proyecto especificadas en requirements.txt
RUN . myenv/bin/activate && pip install -r requirements.txt

# Expone el puerto 80 del contenedor
EXPOSE 80

# Ejecuta el script start.sh cuando se inicie el contenedor
# CMD ["./start.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
