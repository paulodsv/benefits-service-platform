from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import query

router = APIRouter()

class AssignBenefit(BaseModel):
    employee_id: int
    benefit_type: str
    amount: float

@router.post("/assign", status_code=201)
def assign_benefit(payload: AssignBenefit):
    sql = '''
    INSERT INTO balances (employee_id, benefit_type, amount)
    VALUES (%s, %s, %s)
    ON CONFLICT (employee_id, benefit_type) DO UPDATE
      SET amount = balances.amount + EXCLUDED.amount,
          updated_at = now()
    RETURNING id, employee_id, benefit_type, amount
    '''
    row = query(sql, (payload.employee_id, payload.benefit_type, payload.amount), fetchone=True, commit=True)
    return {"id": row[0], "employee_id": row[1], "benefit_type": row[2], "amount": float(row[3])}

@router.get("/{employee_id}/balance")
def get_balances(employee_id: int):
    sql = "SELECT benefit_type, amount FROM balances WHERE employee_id = %s"
    rows = query(sql, (employee_id,), fetchall=True)
    return [{"benefit_type": r[0], "amount": float(r[1])} for r in rows]
