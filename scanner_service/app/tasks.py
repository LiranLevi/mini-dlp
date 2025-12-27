from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.celery_app import celery_app
from app.db import SessionLocal
from app.models import DataSet, ScanResult
from app.matcher import evaluate

@celery_app.task(name="run_scan")
def run_scan(scan_id: str, tenant_id: str, ds_id: str, text: str):
  db: Session = SessionLocal()
  try:
    ds = db.execute(
      select(DataSet).where(DataSet.id == ds_id, DataSet.tenant_id == tenant_id)
    ).scalar_one_or_none()

    sr = db.execute(select(ScanResult).where(ScanResult.id == scan_id, ScanResult.tenant_id == tenant_id)).scalar_one_or_none()
    if not sr:
      return

    if not ds:
      sr.scan_prediction = "failed"
      sr.finished_at = func.now()
      db.commit()
      return

    result_json, found_ids, prediction = evaluate(text, ds.policy)

    sr.scan_prediction = prediction
    sr.result = result_json
    sr.raw_scan_result = str(result_json)
    sr.found_data_types = found_ids
    sr.finished_at = func.now()

    db.commit()
  finally:
    db.close()