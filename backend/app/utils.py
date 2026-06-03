# Бизнес-логика
from datetime import datetime

COURIER_COEFF = {"foot": 2, "bike": 5, "car": 9}
COURIER_CAPACITY = {"foot": 10, "bike": 15, "car": 50}


def parse_time_range(r: str) -> tuple:
    s, e = r.split("-")
    return (datetime.strptime(s, "%H:%M").time(), datetime.strptime(e, "%H:%M").time())


def hours_overlap(a: str, b: str) -> bool:
    a_s, a_e = parse_time_range(a)
    b_s, b_e = parse_time_range(b)
    return a_s <= b_e and b_s <= a_e


def calculate_rating(orders):
    if not orders:
        return None
    region_times = {}
    for o in orders:
        if o.region not in region_times:
            region_times[o.region] = []
    # Время доставки = completion_time - assign_time (или prev completion)
    for i, o in enumerate(orders):
        prev_time = orders[i - 1].completion_time if i > 0 else o.assign_time
        duration = (o.completion_time - prev_time).total_seconds()
        region_times[o.region].append(duration)

    avg_times = [sum(t) / len(t) for t in region_times.values() if t]
    if not avg_times:
        return None
    t_min = min(avg_times)
    rating = (3600 - min(t_min, 3600)) / 3600 * 5
    return round(rating, 2)


def calculate_earnings(orders):
    total = 0
    for o in orders:
        coeff = COURIER_COEFF.get(o.courier_type_at_assign, 2)
        total += 500 * coeff
    return total