import uuid
from datetime import datetime
from typing import Optional, Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func


class Base(DeclarativeBase):
  pass


class DataSet(Base):
  """
  Read-only model for data_sets (owned by policy service).
  We define it here so the scanner can query it, but we won't create it from this service.
  """
  __tablename__ = "data_sets"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
  tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
  name: Mapped[str] = mapped_column(String, nullable=False)
  policy: Mapped[list] = mapped_column(JSONB, nullable=False)


class ScanResult(Base):
  __tablename__ = "scan_results"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
  ds_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

  raw_scan_result: Mapped[Optional[str]] = mapped_column(String, nullable=True)
  scan_prediction: Mapped[str] = mapped_column(String, nullable=False, default="pending")  # pending|match|not matched|failed
  found_data_types: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=False, default=list)
  result: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)