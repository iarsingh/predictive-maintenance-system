REQUIRED = ("vibration", "temp_c", "hours",)
WEIGHTS = {"vibration": 2.0, "temp_c": 0.05, "hours": 0.001}
INTERCEPT = -6.0
THRESHOLD = 0.0


class InputError(ValueError):
    pass


def score(body):
    missing = [name for name in REQUIRED if name not in body]
    if missing:
        raise InputError("missing " + ", ".join(missing))
    total = INTERCEPT
    parts = []
    for name, weight in WEIGHTS.items():
        value = body[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InputError(f"{name} must be a number")
        contrib = weight * value
        total += contrib
        parts.append({"feature": name, "contribution": round(contrib, 4)})
    label = "inspect" if total >= THRESHOLD else "ok"
    return {"score": round(total, 4), "label": label, "threshold": THRESHOLD, "parts": parts}
