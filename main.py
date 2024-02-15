from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from controller.compra import routerCompra
from controller.venta import routerVenta
from controller.guia_remision import routerGuiaRemision
from controller.finanzas import routerFinanzas

load_dotenv()

base_path_compra = "/api/v1/compra"
base_path_venta = "/api/v1/venta"
base_path_guia_remision = "/api/v1/guiaremision"
base_path_finanzas = "/api/v1/finanzas"

app = FastAPI(
    openapi_url="/openapi.json",  # Ruta personalizada para el archivo OpenAPI JSON
    redoc_url=None,  # Desactiva la interfaz ReDoc si no es necesario
    docs_url="/docs",
)
app.include_router(routerCompra, prefix=base_path_compra)
app.include_router(routerVenta, prefix=base_path_venta)
app.include_router(routerGuiaRemision, prefix=base_path_guia_remision)
app.include_router(routerFinanzas, prefix=base_path_finanzas)

origins = [origin.strip() for origin in os.getenv("ORIGINS", "").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def index():
    return JSONResponse({"message": "FAST API"})




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
