# Utiliza la imagen base de Ubuntu 20.04
FROM ubuntu:20.04

RUN apt-get update -y

RUN DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common

RUN apt install python3-pip -y

RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt update -y

RUN apt install python3.12 -y

RUN apt install wget -y

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

RUN apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb -y

RUN apt-get install python3.12-venv python3.12-dev -y

WORKDIR /app

COPY . /app

RUN python3.12 -m venv myenv

RUN source myenv/bin/activate

RUN python --version

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

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
