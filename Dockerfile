# Utiliza la imagen base de Ubuntu 20.04
FROM  ubuntu:20.04

# Actualiza la lista de paquetes e instala dependencias
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
        wget \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Añade el repositorio de deadsnakes y actualiza
RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update -y

# Instala Python 3.12 y herramientas relacionadas
RUN apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        python3.12-dev

# Descarga e instala wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb -y \
    && rm wkhtmltox_0.12.6-1.focal_amd64.deb

# RUN apt-get update -y

# RUN DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common

# RUN apt install python3-pip -y

# RUN add-apt-repository ppa:deadsnakes/ppa -y

# RUN apt update -y

# RUN apt install python3.12 -y

# RUN apt install wget -y

# RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

# RUN apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb -y

# RUN apt-get install python3.12-venv python3.12-dev -y

WORKDIR /app

COPY . /app

# Crea y activa el entorno virtual
RUN python3.12 -m venv myenv

# Copia el script de inicio al directorio de trabajo
COPY start.sh .

# Otorga permisos de ejecución al script
RUN chmod +x start.sh

# Instala las dependencias desde requirements.txt
RUN . myenv/bin/activate && pip install -r requirements.txt

EXPOSE 80

# Configura el comando principal para ejecutar el script de inicio
CMD ["./start.sh"]

# # Usa una imagen oficial de Python 3.12 como base
# FROM python:3.12-slim

# # Establece el directorio de trabajo en /app
# WORKDIR /app

# # Copia el código actual al contenedor en /app
# COPY . /app

# RUN apt-get update && apt-get upgrade -y

# # Instala las dependencias especificadas en requirements.txt, wget y xvfb
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends wget xvfb libjpeg-turbo8 libssl1.1 \
#     && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
#     && apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb \
#     && wkhtmltopdf --version \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* \
#     && pip install --no-cache-dir -r requirements.txt \
#     && rm wkhtmltox_0.12.6-1.focal_amd64.deb

# # Expone el puerto 80 en el contenedor
# EXPOSE 80

# # Comando para ejecutar la aplicación
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
