from uuid import UUID
from pydantic import BaseModel

class ScanTrigger(BaseModel):
  tenant_id: UUID
  ds_id: UUID
  input: str

class ScanIdOut(BaseModel):
  scan_id: UUID