from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db, engine
from app.models import Base, DataSet
from app.schemas import DataSetCreate, DataSetOut

app = FastAPI(title="Policy Service")

@app.on_event("startup")
def startup():
  Base.metadata.create_all(bind=engine)

@app.post("/internal/data-sets", response_model=DataSetOut, status_code=201)
def create_ds(payload: DataSetCreate, db: Session = Depends(get_db)):
  ds = DataSet(tenant_id=payload.tenant_id, name=payload.name, policy=[p.model_dump(mode="json") for p in payload.policy])
  db.add(ds)
  db.commit()
  db.refresh(ds)
  return ds

@app.get("/internal/data-sets/{ds_id}", response_model=DataSetOut)
def get_ds(ds_id: str, tenant_id: str, db: Session = Depends(get_db)):
  ds = db.query(DataSet).filter(DataSet.id == ds_id, DataSet.tenant_id == tenant_id).first()
  if not ds:
    raise HTTPException(status_code=404, detail="Not found")
  return ds