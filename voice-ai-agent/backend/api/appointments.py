from __future__ import annotations

import datetime as dt
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from scheduler import appointment_engine as engine


router = APIRouter(prefix="/appointments", tags=["appointments"])


class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    specialty: str
    date: dt.date
    time: dt.time


class AppointmentBookResponse(BaseModel):
    success: bool
    error: str | None = None


class SlotOut(BaseModel):
    time: dt.time


@router.get("/availability/{doctor_id}/{date}", response_model=List[SlotOut])
def get_availability(doctor_id: str, date: dt.date):
    slots = engine.get_available_slots(doctor_id=doctor_id, date=date)
    return [SlotOut(time=s.time) for s in slots]


@router.post("/book", response_model=AppointmentBookResponse)
def book_appointment(payload: AppointmentCreate):
    ok, err = engine.book_appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        specialty=payload.specialty,
        date=payload.date,
        time_=payload.time,
    )
    return AppointmentBookResponse(success=ok, error=err)


@router.post("/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    ok = engine.cancel_appointment(appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Appointment not found or already cancelled")
    return {"success": True}


class RescheduleRequest(BaseModel):
    new_date: dt.date
    new_time: dt.time


@router.post("/{appointment_id}/reschedule")
def reschedule_appointment(appointment_id: int, payload: RescheduleRequest):
    ok, err = engine.reschedule_appointment(
        appointment_id=appointment_id,
        new_date=payload.new_date,
        new_time=payload.new_time,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=err or "Unable to reschedule")
    return {"success": True}

