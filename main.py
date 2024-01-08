from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


from controller.compra import routerCompra
from controller.venta import routerVenta
from controller.guia_remision import routerGuiaRemision


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

base_path_compra = "/api/v1/compra"
base_path_venta = "/api/v1/venta"
base_path_guia_remision = "/api/v1/guiaremision"

app.include_router(routerCompra, prefix=base_path_compra)
app.include_router(routerVenta, prefix=base_path_venta)
app.include_router(routerGuiaRemision, prefix=base_path_guia_remision)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def index():
    return JSONResponse({"message": "FAST API"})



