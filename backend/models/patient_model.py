from __future__ import annotations
from datetime import datetime
from typing import List
from sqlalchemy import Integer,  String, Column, ForeignKey, func,DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.extensions import db


class PatientDemographic(db.Model):
    __tablename__ = "patientdemographics"
    id: Mapped[int] = mapped_column(primary_key=True)
    fname: Mapped[str] = Column(String(255))
    mname: Mapped[str] = Column(String(255))
    lname: Mapped[str] = Column(String(255))
    dob: Mapped[datetime] = mapped_column(datetime)
    gender: Mapped[str] = Column(String(10))
    phoneNo: Mapped[str] = Column(String(12))
    phoneNo1: Mapped[str] = Column(String(12))
    uhid: Mapped[str] = Column(String(50))


class Patient(db.Model):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    patientdemographic_id: Mapped[int] = mapped_column(ForeignKey('patientdemographics.id'))
    diagnosis: Mapped[str] = Column(String(255))
    plan: Mapped[str] = Column(String(255))
    eye: Mapped[str] = Column(String(10))
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
        return f'Patient({self.id}, "{self.name}")'