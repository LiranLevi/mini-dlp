import os
import requests
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db, engine
from app.models import Base, DataType
from app.schemas import DataTypeCreate, DataTypeOut, DataSetCreate, DataSetOut

POLICY_URL = os.environ["POLICY_SERVICE_URL"]

app = FastAPI(title="Configuration Service")

@app.on_event("startup")
def startup():
  Base.metadata.create_all(bind=engine)

@app.post("/data-types", response_model=DataTypeOut, status_code=201)
def create_dt(payload: DataTypeCreate, db: Session = Depends(get_db)):
  if payload.type != "keywords":
    raise HTTPException(status_code=400, detail="Only type=keywords supported")
  if payload.threshold < 1:
    raise HTTPException(status_code=400, detail="threshold must be >= 1")

  dt = DataType(
    name=payload.name,
    description=payload.description,
    type=payload.type,
    content=payload.content,
    threshold=payload.threshold,
  )
  db.add(dt)
  db.commit()
  db.refresh(dt)
  return dt

@app.get("/data-types/{dt_id}", response_model=DataTypeOut)
def get_dt(dt_id: str, db: Session = Depends(get_db)):
  dt = db.query(DataType).filter(DataType.id == dt_id).first()
  if not dt:
    raise HTTPException(status_code=404, detail="Not found")
  return dt

@app.post("/data-sets", response_model=DataSetOut, status_code=201)
def create_ds(payload: DataSetCreate, db: Session = Depends(get_db)):
  if not payload.data_type_ids:
    raise HTTPException(status_code=400, detail="data_type_ids must not be empty")

  dts = db.query(DataType).filter(DataType.id.in_(payload.data_type_ids)).all()
  if len(dts) != len(payload.data_type_ids):
    raise HTTPException(status_code=400, detail="One or more data_type_ids not found")

  policy = [{"id": str(dt.id), "name": dt.name, "content": dt.content, "threshold": dt.threshold} for dt in dts]

  r = requests.post(f"{POLICY_URL}/internal/data-sets", json={
    "tenant_id": str(payload.tenant_id),
    "name": payload.name,
    "policy": policy
  }, timeout=10)

  if r.status_code >= 400:
    raise HTTPException(status_code=502, detail=f"Policy service error: {r.text}")

  return r.json()

@app.get("/data-sets/{ds_id}", response_model=DataSetOut)
def get_ds(ds_id: str, tenant_id: str):
  r = requests.get(f"{POLICY_URL}/internal/data-sets/{ds_id}", params={"tenant_id": tenant_id}, timeout=10)
  if r.status_code == 404:
    raise HTTPException(status_code=404, detail="Not found")
  if r.status_code >= 400:
    raise HTTPException(status_code=502, detail=f"Policy service error: {r.text}")
  return r.json()