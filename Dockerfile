# Usa una imagen oficial de Python 3.12 como base
FROM python:3

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código actual al contenedor en /app
COPY . /app

# Instala las dependencias especificadas en requirements.txt, wget y xvfb
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget xvfb libjpeg-turbo8 libssl1.1 \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb \
    && wkhtmltopdf --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && rm wkhtmltox_0.12.6-1.focal_amd64.deb

# Expone el puerto 80 en el contenedor
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
