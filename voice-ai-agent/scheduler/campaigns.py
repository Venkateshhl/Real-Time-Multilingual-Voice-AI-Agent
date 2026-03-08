from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import List


@dataclass
class OutboundCall:
    patient_id: str
    phone_number: str
    scheduled_at: dt.datetime
    message: str


_OUTBOUND_QUEUE: List[OutboundCall] = []


def schedule_reminder(patient_id: str, phone_number: str, scheduled_at: dt.datetime, message: str) -> OutboundCall:
    """
    Very lightweight in-memory outbound campaign scheduler.
    In a real deployment this would enqueue into a message broker or
    connect to a telephony provider (e.g., Twilio).
    """
    call = OutboundCall(
        patient_id=patient_id,
        phone_number=phone_number,
        scheduled_at=scheduled_at,
        message=message,
    )
    _OUTBOUND_QUEUE.append(call)
    return call


def list_scheduled_calls() -> List[OutboundCall]:
    return list(_OUTBOUND_QUEUE)

