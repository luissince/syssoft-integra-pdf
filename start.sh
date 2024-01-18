#!/bin/bash

# Activa el entorno virtual
. myenv/bin/activate

# Ejecuta tu aplicación con Uvicorn
uvicorn main:app --host 0.0.0.0 --port 80