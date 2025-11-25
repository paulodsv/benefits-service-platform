from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.db import query

router = APIRouter()

class EmployeeCreate(BaseModel):
    company_id: int
    name: str
    document: Optional[str] = None

@router.post("/", status_code=201)
def create_employee(payload: EmployeeCreate):
    sql = "INSERT INTO employees (company_id, name, document) VALUES (%s, %s, %s) RETURNING id, company_id, name, status"
    row = query(sql, (payload.company_id, payload.name, payload.document), fetchone=True, commit=True)
    return {"id": row[0], "company_id": row[1], "name": row[2], "status": row[3]}

@router.get("/")
def list_employees(company_id: int = Query(...), status: Optional[str] = Query(None)):
    params = [company_id]
    sql = "SELECT id, company_id, name, status FROM employees WHERE company_id = %s"
    if status:
        sql += " AND status = %s"
        params.append(status)
    rows = query(sql, tuple(params), fetchall=True)
    return [{"id": r[0], "company_id": r[1], "name": r[2], "status": r[3]} for r in rows]
