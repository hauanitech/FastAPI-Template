from sqlalchemy import Column, String, UUID

from database import Base


class TableBase(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, index=True)
    created_at = Column(String)
    updated_at = Column(String)