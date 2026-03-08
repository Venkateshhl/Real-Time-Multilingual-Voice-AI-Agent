from scheduler.appointment_engine.engine import check_availability, book_appointment, cancel_appointment, reschedule_appointment

def call_tool(action):
    intent = action.get('intent')
    if intent == 'book_appointment':
        return book_appointment(
            patient=action.get('patient', 'default_patient'),
            doctor=action.get('doctor'),
            date=action.get('date'),
            time=action.get('time')
        )
    elif intent == 'cancel_appointment':
        return cancel_appointment(
            patient=action.get('patient', 'default_patient'),
            doctor=action.get('doctor'),
            date=action.get('date'),
            time=action.get('time')
        )
    elif intent == 'reschedule_appointment':
        return reschedule_appointment(
            patient=action.get('patient', 'default_patient'),
            doctor=action.get('doctor'),
            old_date=action.get('old_date'),
            new_date=action.get('new_date'),
            time=action.get('time')
        )
    elif intent == 'check_availability':
        return check_availability(
            doctor=action.get('doctor'),
            date=action.get('date')
        )
    else:
        return "I'm sorry, I didn't understand that request."