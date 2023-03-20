def string_convert_to_number(payload: str) -> str:
    try:
        if payload.isdigit():
            return payload
        payload = float(payload)
        return str(round(payload, 2))
    except ValueError:
        raise ValueError("payload is not a number")
