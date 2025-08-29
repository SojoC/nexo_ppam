from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from app.db.base import Base

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), index=True)
    last_name: Mapped[str] = mapped_column(String(80), index=True)
    phone: Mapped[str | None] = mapped_column(String(20), index=True)
    address: Mapped[str | None] = mapped_column(String(200))

    circuit_id: Mapped[int | None] = mapped_column(ForeignKey("circuits.id", ondelete="SET NULL"), index=True)
    congregation_id: Mapped[int | None] = mapped_column(ForeignKey("congregations.id", ondelete="SET NULL"), index=True)
    territory_id: Mapped[int | None] = mapped_column(ForeignKey("territories.id", ondelete="SET NULL"), index=True)

    congregation: Mapped["Congregation" | None] = relationship(back_populates="contacts")
    territory: Mapped["Territory" | None] = relationship(back_populates="contacts")
