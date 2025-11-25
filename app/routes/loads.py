from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import pika
from app.db import query
from app.config import RABBITMQ_URL

router = APIRouter()

class LoadItem(BaseModel):
    employee_id: int
    amount: float

class LoadCreate(BaseModel):
    company_id: int
    items: list[LoadItem]

@router.post("/", status_code=201)
def create_load(payload: LoadCreate):
    total_items = len(payload.items)
    amount_total = sum(i.amount for i in payload.items)
    sql = "INSERT INTO loads (company_id, total_items, amount_total, status) VALUES (%s,%s,%s,'pending') RETURNING id"
    row = query(sql, (payload.company_id, total_items, amount_total), fetchone=True, commit=True)
    load_id = row[0]
    for it in payload.items:
        query("INSERT INTO load_items (load_id, employee_id, amount, status) VALUES (%s,%s,%s,'pending')",
              (load_id, it.employee_id, it.amount), commit=True)
    # publish message
    params = pika.URLParameters(RABBITMQ_URL)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue='benefit.load.request', durable=True)
    ch.basic_publish(exchange='', routing_key='benefit.load.request', body=json.dumps({"load_id": load_id}),
                     properties=pika.BasicProperties(delivery_mode=2))
    conn.close()
    return {"load_id": load_id, "status": "queued"}

@router.get("/{load_id}/status")
def get_status(load_id: int):
    sql = "SELECT id, company_id, total_items, amount_total, status, created_at FROM loads WHERE id=%s"
    row = query(sql, (load_id,), fetchone=True)
    if not row:
        raise HTTPException(404, "load not found")
    return {"id": row[0], "company_id": row[1], "total_items": row[2], "amount_total": float(row[3]), "status": row[4], "created_at": row[5]}
