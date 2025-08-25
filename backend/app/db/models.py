from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str | None] = mapped_column(String)
    telefono: Mapped[str | None] = mapped_column(String)
    circuito: Mapped[str | None] = mapped_column(String)
    congregacion: Mapped[str | None] = mapped_column(String)
    territorio: Mapped[str | None] = mapped_column(String)
    privilegios: Mapped[str | None] = mapped_column(String)
    metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
