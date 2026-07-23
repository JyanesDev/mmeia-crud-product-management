from fastapi import FastAPI

from src.routers import categorias, productos

# Bumped on each deployment milestone (03_Preparar_Despliegue, Paso 6 point 3:
# "consulta la version reportada por la app y comparala con la esperada").
APP_VERSION = "0.3.0"

app = FastAPI(title="mmeia-crud-product-management", version=APP_VERSION)

app.include_router(categorias.router)
app.include_router(productos.router)


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}
