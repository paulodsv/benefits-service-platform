from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import query

router = APIRouter()

class CompanyCreate(BaseModel):
    name: str

@router.post("/", status_code=201)
def create_company(payload: CompanyCreate):
    sql = "INSERT INTO companies (name) VALUES (%s) RETURNING id, name, created_at"
    row = query(sql, (payload.name,), fetchone=True, commit=True)
    if row:
        return {"id": row[0], "name": row[1], "created_at": row[2]}
    raise HTTPException(500, "cannot create")

@router.get("/{company_id}")
def get_company(company_id: int):
    sql = "SELECT id, name, created_at FROM companies WHERE id=%s"
    row = query(sql, (company_id,), fetchone=True)
    if not row:
        raise HTTPException(404, "company not found")
    return {"id": row[0], "name": row[1], "created_at": row[2]}
