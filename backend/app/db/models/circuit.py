from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app.db.base import Base

class Circuit(Base):
    __tablename__ = "circuits"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    code: Mapped[str | None] = mapped_column(String(32), unique=True, index=True)
    congregations: Mapped[list["Congregation"]] = relationship(
        back_populates="circuit", cascade="all, delete-orphan"
    )
