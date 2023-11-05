from __future__ import annotations
from datetime import datetime
from typing import List
from sqlalchemy import Integer,  String, Column, ForeignKey, func,DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.extensions import db

class Patient(db.Model):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Column(String(255))
    age: Mapped[int] = Column(Integer)
    gender: Mapped[str] = Column(String(10))
    uhid: Mapped[str] = Column(String(50))
    phoneNo: Mapped[str] = Column(String(15))
    diagnosis: Mapped[str] = Column(String(255))
    plan: Mapped[str] = Column(String(255))
    oneEyed: Mapped[str] = Column(String(10))
    priority: Mapped[str] = Column(String(20))
    anesthesia: Mapped[str] = Column(String(50))
    cabin: Mapped[str] = Column(String(50))
    adviceBy: Mapped[str] = Column(String(255))
    initialDate: Mapped[datetime] = Column(DateTime)
    finalDate: Mapped[datetime] = Column(DateTime)
    eua: Mapped[str] = Column(String(255))
    short: Mapped[str] = Column(String(255))
    remark: Mapped[str] = Column(String(255))

    def __repr__(self):
        return f'Role({self.id}, "{self.name}")'