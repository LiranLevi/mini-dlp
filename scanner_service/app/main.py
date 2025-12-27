from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db import engine, SessionLocal
from app.models import ScanResult
from app.schemas import ScanTrigger, ScanIdOut
from app.tasks import run_scan

app = FastAPI(title="Scanner Service")

@app.on_event("startup")
def startup():
  # create only scan_results table from this service
  ScanResult.__table__.create(bind=engine, checkfirst=True)

@app.post("/scans", response_model=ScanIdOut, status_code=202)
def trigger_scan(payload: ScanTrigger):
  db: Session = SessionLocal()
  try:
    sr = ScanResult(tenant_id=payload.tenant_id, ds_id=payload.ds_id, scan_prediction="pending")
    db.add(sr)
    db.commit()
    db.refresh(sr)

    run_scan.delay(str(sr.id), str(payload.tenant_id), str(payload.ds_id), payload.input)
    return {"scan_id": sr.id}
  finally:
    db.close()

@app.get("/scans/{scan_id}")
def poll_scan(scan_id: str, tenant_id: str):
  db: Session = SessionLocal()
  try:
    sr = db.query(ScanResult).filter(ScanResult.id == scan_id, ScanResult.tenant_id == tenant_id).first()
    if not sr:
      raise HTTPException(status_code=404, detail="Not found")

    if sr.scan_prediction == "pending":
      return {"status": "pending"}

    if sr.scan_prediction == "failed":
      raise HTTPException(status_code=500, detail="Scan failed")

    if sr.scan_prediction == "match":
      return sr.result
    return {"status": "not matched"}
  finally:
    db.close()