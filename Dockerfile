FROM python:3.12

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    libjpeg-turbo8 \
    libssl1.1

# Descargar e instalar wkhtmltopdf 0.12.6
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb \
    && rm ./wkhtmltox_0.12.6-1.focal_amd64.deb

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código actual al contenedor en /app
COPY . /app

RUN pip install --upgrade pip

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

RUN python3 --version 

# Expone el puerto 80 en el contenedor
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
