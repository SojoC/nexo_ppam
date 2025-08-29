from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from app.db.base import Base

class Congregation(Base):
    __tablename__ = "congregations"
    __table_args__ = (UniqueConstraint("name", "circuit_id", name="uq_congregations_name_circuit"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    circuit_id: Mapped[int] = mapped_column(ForeignKey("circuits.id", ondelete="CASCADE"), index=True)

    circuit: Mapped["Circuit"] = relationship(back_populates="congregations")
    territories: Mapped[list["Territory"]] = relationship(back_populates="congregation", cascade="all, delete-orphan")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="congregation")
