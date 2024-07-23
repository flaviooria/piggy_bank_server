def generate_token() -> str:
    import uuid

    return str(uuid.uuid4())[:6]
