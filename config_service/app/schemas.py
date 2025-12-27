from uuid import UUID
from pydantic import BaseModel, Field

class DataTypeCreate(BaseModel):
  name: str
  description: str = ""
  type: str = "keywords"
  content: list[str] = Field(default_factory=list)
  threshold: int = 1

class DataTypeOut(BaseModel):
  id: UUID
  name: str
  description: str
  type: str
  content: list[str]
  threshold: int

class DataSetCreate(BaseModel):
  tenant_id: UUID
  name: str
  data_type_ids: list[UUID]

class DataSetOut(BaseModel):
  id: UUID
  tenant_id: UUID
  name: str
  policy: list[dict]