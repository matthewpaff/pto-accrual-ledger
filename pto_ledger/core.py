"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value

def accrue_months(data):
    import re
    from datetime import date
    fields(data, ("start_month", "opening_minutes", "earn_minutes", "cap_minutes", "used_minutes"))
    start = data["start_month"]
    if not isinstance(start, str) or not re.fullmatch(r"\d{4}-\d{2}-01", start):
        raise ValueError("Use YYYY-MM-01")
    stamp = date.fromisoformat(start)
    if not 2000 <= stamp.year <= 2090:
        raise ValueError("Unsupported start year")
    balance = integer(data["opening_minutes"], 0, 10**7)
    earn = integer(data["earn_minutes"], 0, 10**7)
    cap = integer(data["cap_minutes"], 1, 10**7)
    usage = sequence(data["used_minutes"], 36)
    if balance > cap:
        raise ValueError("Opening balance exceeds cap")
    rows = []
    for offset, used in enumerate(usage):
        used = integer(used, 0, 10**7)
        credited = min(earn, cap - balance)
        balance += credited
        if used > balance:
            raise ValueError("Usage exceeds available balance")
        balance -= used
        month_index = stamp.year * 12 + stamp.month - 1 + offset
        month = date(month_index // 12, month_index % 12 + 1, 1).isoformat()
        rows.append({"month": month, "earned_minutes": credited, "used_minutes": used, "closing_minutes": balance})
    return {"months": rows, "closing_minutes": balance}
