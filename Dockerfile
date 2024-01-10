# Usa una imagen oficial de Python 3.12 como base
FROM python:3.12-buster


RUN apt-get update \
    && apt-get install -y \
        curl \
        libxrender1 \
        libjpeg62-turbo \
        fontconfig \
        libxtst6 \
        xfonts-75dpi \
        xfonts-base \
        xz-utils
RUN curl "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb" -L -o "wkhtmltopdf.deb"

RUN dpkg -i wkhtmltopdf.deb

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código actual al contenedor en /app
COPY . /app

RUN pip install --upgrade pip

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

# Expone el puerto 80 en el contenedor
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
