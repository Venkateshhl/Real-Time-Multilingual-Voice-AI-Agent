from __future__ import annotations

import datetime as dt

from fastapi import APIRouter
from pydantic import BaseModel

from scheduler import campaigns


router = APIRouter(prefix="/campaigns", tags=["campaigns"])


class ReminderRequest(BaseModel):
    patient_id: str
    phone_number: str
    appointment_datetime: dt.datetime


@router.post("/reminder")
def schedule_appointment_reminder(payload: ReminderRequest):
    """
    Schedule an outbound reminder call for an upcoming appointment.
    """
    message = (
        "This is a reminder about your upcoming appointment. "
        "If you would like to reschedule or cancel, you can do so during the call."
    )
    call = campaigns.schedule_reminder(
        patient_id=payload.patient_id,
        phone_number=payload.phone_number,
        scheduled_at=payload.appointment_datetime,
        message=message,
    )
    return {"scheduled": True, "scheduled_at": call.scheduled_at}

