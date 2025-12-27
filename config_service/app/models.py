import uuid
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func


class Base(DeclarativeBase):
  pass


class DataType(Base):
  __tablename__ = "data_types"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String, nullable=False)
  description: Mapped[str] = mapped_column(String, nullable=False, default="")
  type: Mapped[str] = mapped_column(String, nullable=False, default="keywords")
  content: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
  threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False
  )