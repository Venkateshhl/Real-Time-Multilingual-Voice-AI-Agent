from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    Time,
    create_engine,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


DATABASE_URL = "sqlite:///./appointments.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    doctor_id = Column(String, index=True)
    specialty = Column(String, index=True)
    date = Column(Date, index=True)
    time = Column(Time, index=True)
    status = Column(String, default="booked")  # booked / cancelled


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedule"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String, index=True)
    date = Column(Date, index=True)
    slot = Column(Time, index=True)


Base.metadata.create_all(bind=engine)


@dataclass
class Slot:
    time: dt.time


def get_db() -> Session:
    return SessionLocal()


def get_available_slots(doctor_id: str, date: dt.date) -> List[Slot]:
    """
    Return all open slots for a doctor on a given date,
    excluding those already booked.
    """
    db = get_db()
    try:
        all_slots = db.execute(
            select(DoctorSchedule.slot).where(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.date == date,
            )
        ).scalars().all()

        booked_slots = db.execute(
            select(Appointment.time).where(
                Appointment.doctor_id == doctor_id,
                Appointment.date == date,
                Appointment.status == "booked",
            )
        ).scalars().all()

        booked_set = {t for t in booked_slots}
        free = [Slot(time=s) for s in all_slots if s not in booked_set]
        return free
    finally:
        db.close()


def book_appointment(
    patient_id: str,
    doctor_id: str,
    specialty: str,
    date: dt.date,
    time_: dt.time,
) -> tuple[bool, Optional[str]]:
    """
    Try to book an appointment. Returns (success, error_message).
    Performs conflict checks and past-time validation.
    """
    now = dt.datetime.now()
    appt_dt = dt.datetime.combine(date, time_)
    if appt_dt <= now:
        return False, "Cannot book an appointment in the past."

    db = get_db()
    try:
        # Check that slot is part of doctor's schedule.
        schedule_exists = db.execute(
            select(DoctorSchedule).where(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.date == date,
                DoctorSchedule.slot == time_,
            )
        ).first()
        if not schedule_exists:
            return False, "Requested slot is not in doctor's schedule."

        # Check for double booking.
        conflict = db.execute(
            select(Appointment).where(
                Appointment.doctor_id == doctor_id,
                Appointment.date == date,
                Appointment.time == time_,
                Appointment.status == "booked",
            )
        ).first()
        if conflict:
            return False, "Slot already booked."

        appt = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            specialty=specialty,
            date=date,
            time=time_,
            status="booked",
        )
        db.add(appt)
        db.commit()
        return True, None
    finally:
        db.close()


def cancel_appointment(appointment_id: int) -> bool:
    db = get_db()
    try:
        appt = db.get(Appointment, appointment_id)
        if not appt or appt.status != "booked":
            return False
        appt.status = "cancelled"
        db.commit()
        return True
    finally:
        db.close()


def reschedule_appointment(
    appointment_id: int,
    new_date: dt.date,
    new_time: dt.time,
) -> tuple[bool, Optional[str]]:
    db = get_db()
    try:
        appt: Appointment | None = db.get(Appointment, appointment_id)
        if not appt or appt.status != "booked":
            return False, "Appointment not found or not active."

        ok, err = book_appointment(
            patient_id=appt.patient_id,
            doctor_id=appt.doctor_id,
            specialty=appt.specialty,
            date=new_date,
            time_=new_time,
        )
        if not ok:
            return False, err

        # Mark old appointment as cancelled.
        appt.status = "cancelled"
        db.commit()
        return True, None
    finally:
        db.close()

