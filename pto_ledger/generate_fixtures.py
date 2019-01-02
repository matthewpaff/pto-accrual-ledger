"""Original generated examples with independent expected results."""

def make_case(index):
    earn = 60 + index
    data = {"start_month": "2019-01-01", "opening_minutes": 0, "earn_minutes": earn, "cap_minutes": 10000, "used_minutes": [0]}
    kind = index % 8
    rows = [{"month": "2019-01-01", "earned_minutes": earn, "used_minutes": 0, "closing_minutes": earn}]
    closing, description = earn, "credit integer-minute accrual for one calendar month"
    if kind == 1:
        data.update(start_month="2019-12-01", earn_minutes=60, used_minutes=[0, 30])
        rows = [{"month": "2019-12-01", "earned_minutes": 60, "used_minutes": 0, "closing_minutes": 60},
                {"month": "2020-01-01", "earned_minutes": 60, "used_minutes": 30, "closing_minutes": 90}]
        closing, description = 90, "carry balances across a December to January boundary"
    elif kind == 2:
        data.update(opening_minutes=90, earn_minutes=30, cap_minutes=100, used_minutes=[20])
        rows = [{"month": "2019-01-01", "earned_minutes": 10, "used_minutes": 20, "closing_minutes": 80}]
        closing, description = 80, "cap accrual before subtracting monthly usage"
    elif kind == 3:
        data.update(opening_minutes=index, used_minutes=[])
        rows, closing, description = [], index, "preserve opening balance when no months are requested"
    elif kind == 4:
        data["used_minutes"] = [10001]
        description = "reject usage that exceeds the available balance"
    elif kind == 5:
        data["start_month"] = "2019-01-15"
        description = "require a first-of-month start date"
    elif kind == 6:
        data["used_minutes"] = [True]
        description = "reject boolean monthly usage values"
    elif kind == 7:
        data.update(start_month="2020-01-01", earn_minutes=10, used_minutes=[0, 0, 0])
        rows = [{"month": "2020-" + month + "-01", "earned_minutes": 10, "used_minutes": 0, "closing_minutes": balance}
                for month, balance in (("01", 10), ("02", 20), ("03", 30))]
        closing, description = 30, "advance date-only accrual through leap-year February"
    case = {"id": "pto-{:04d}".format(index), "description": description, "input": data}
    case.update({"expected_error": True} if kind in (4, 5, 6) else {"expected": {"months": rows, "closing_minutes": closing}})
    return case
