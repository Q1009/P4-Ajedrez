import uuid

def generate_unique_id():
    base = str(uuid.uuid4())
    id = base[9:13]
    return id