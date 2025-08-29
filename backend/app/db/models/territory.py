from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from app.db.base import Base

class Territory(Base):
    __tablename__ = "territories"
    __table_args__ = (UniqueConstraint("name", "congregation_id", name="uq_territories_name_congregation"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    congregation_id: Mapped[int] = mapped_column(ForeignKey("congregations.id", ondelete="CASCADE"), index=True)

    congregation: Mapped["Congregation"] = relationship(back_populates="territories")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="territory")
