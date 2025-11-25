from fastapi import FastAPI
from app.db import init_db_pool
from app.routes import companies, employees, benefits, loads

app = FastAPI(title="Beneficios - Projeto")

@app.on_event("startup")
def startup():
    init_db_pool()
    app.include_router(companies.router, prefix="/companies", tags=["companies"])
    app.include_router(employees.router, prefix="/employees", tags=["employees"])
    app.include_router(benefits.router, prefix="/benefits", tags=["benefits"])
    app.include_router(loads.router, prefix="/loads", tags=["loads"])

@app.get('/health')
def health():
    return {"status":"ok"}
