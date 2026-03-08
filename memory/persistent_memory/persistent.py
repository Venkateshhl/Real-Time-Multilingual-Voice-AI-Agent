# In-memory persistent storage (use database in production)
persistent_store = {}

def get_persistent(patient_id):
    return persistent_store.get(patient_id, {})

def set_persistent(patient_id, data):
    persistent_store[patient_id] = data