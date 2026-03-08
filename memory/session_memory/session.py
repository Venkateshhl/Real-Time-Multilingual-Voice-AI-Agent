# In-memory session storage (use Redis in production)
session_store = {}

def get_session(session_id):
    return session_store.get(session_id, {})

def set_session(session_id, data):
    session_store[session_id] = data