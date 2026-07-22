from fastapi import FastAPI

from src.routers import categorias, productos

app = FastAPI(title="mmeia-crud-product-management")

app.include_router(categorias.router)
app.include_router(productos.router)


@app.get("/health")
def health():
    return {"status": "ok"}
