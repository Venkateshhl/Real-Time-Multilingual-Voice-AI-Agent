"""
Appointment Engine - Handles appointment booking, cancellation, and rescheduling
"""

# Mock appointment database (in production, use a real database)
appointments = []


def check_availability(doctor, date):
    """Check available time slots for a doctor on a given date"""
    available_slots = ["10:00 AM", "2:00 PM", "4:00 PM"]
    booked = [a['time'] for a in appointments if a['doctor'] == doctor and a['date'] == date]
    return [slot for slot in available_slots if slot not in booked]


def book_appointment(patient, doctor, date, time=None):
    """Book an appointment for a patient with a doctor"""
    if time is None:
        time = "10:00 AM"

    available = check_availability(doctor, date)
    if time in available:
        appointments.append({
            'patient': patient,
            'doctor': doctor,
            'date': date,
            'time': time,
            'status': 'booked'
        })
        return f"Appointment booked successfully for {doctor} on {date} at {time}."
    else:
        available_str = ', '.join(available)
        return f"Sorry, that slot is not available. Available slots: {available_str}"


def cancel_appointment(patient, doctor, date, time):
    """Cancel an existing appointment"""
    for appt in appointments:
        if (appt['patient'] == patient and appt['doctor'] == doctor and
                appt['date'] == date and appt['time'] == time):
            appt['status'] = 'cancelled'
            return "Appointment cancelled successfully."
    return "No matching appointment found."


def reschedule_appointment(patient, doctor, old_date, new_date, time):
    """Reschedule an appointment to a new date"""
    cancel_result = cancel_appointment(patient, doctor, old_date, time)
    if "successfully" in cancel_result:
        return book_appointment(patient, doctor, new_date, time)
    return cancel_result
