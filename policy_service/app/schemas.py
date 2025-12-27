from uuid import UUID
from pydantic import BaseModel, Field

class PolicyDT(BaseModel):
  id: UUID
  name: str
  content: list[str] = Field(default_factory=list)
  threshold: int = 1

class DataSetCreate(BaseModel):
  tenant_id: UUID
  name: str
  policy: list[PolicyDT]

class DataSetOut(BaseModel):
  id: UUID
  tenant_id: UUID
  name: str
  policy: list[PolicyDT]