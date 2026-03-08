pip install openai==0.28  # Or update code to use new APIpip install openai==0.28  # Or update code to use new API# Mock appointment database
appointments = []

def check_availability(doctor, date):
    # Mock available slots
    available_slots = ["10:00 AM", "2:00 PM", "4:00 PM"]
    # In real, check against booked
    booked = [a['time'] for a in appointments if a['doctor'] == doctor and a['date'] == date]
    return [slot for slot in available_slots if slot not in booked]

def book_appointment(patient, doctor, date, time):
    # Check if slot is available
    if time in check_availability(doctor, date):
        appointments.append({
            'patient': patient,
            'doctor': doctor,
            'date': date,
            'time': time,
            'status': 'booked'
        })
        return f"Appointment booked successfully for {doctor} on {date} at {time}."
    else:
        return "Sorry, that slot is not available. Available slots: " + ", ".join(check_availability(doctor, date))

def cancel_appointment(patient, doctor, date, time):
    for appt in appointments:
        if appt['patient'] == patient and appt['doctor'] == doctor and appt['date'] == date and appt['time'] == time:
            appt['status'] = 'cancelled'
            return "Appointment cancelled successfully."
    return "No matching appointment found."

def reschedule_appointment(patient, doctor, old_date, new_date, time):
    # Cancel old and book new
    cancel_result = cancel_appointment(patient, doctor, old_date, time)
    if "successfully" in cancel_result:
        return book_appointment(patient, doctor, new_date, time)
    return cancel_result