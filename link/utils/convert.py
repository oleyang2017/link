def str_to_number(payload: str) -> float:
    try:
        payload = float(payload)
        return round(payload, 2)
    except ValueError:
        raise ValueError("payload is not a number")
