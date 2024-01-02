from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pdfkit
import mysql.connector

from controller.compra import routerCompra


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

base_path_compra = "/api/v1/compra"
app.include_router(routerCompra, prefix=base_path_compra)


templates = Jinja2Templates(directory="templates")

@app.get("/")
def index():
    return "Hello"



