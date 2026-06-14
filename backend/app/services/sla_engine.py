from datetime import datetime, timezone, timedelta

SLA_RULES = {
    "vip":    {"response_hours": 2,  "resolve_hours": 24},
    "key":    {"response_hours": 4,  "resolve_hours": 48},
    "normal": {"response_hours": 8,  "resolve_hours": 72},
}


def calculate_sla(customer_level: str) -> dict:
    rule = SLA_RULES.get(customer_level, SLA_RULES["normal"])
    now = datetime.now(timezone.utc)
    return {
        "sla_response_hours": rule["response_hours"],
        "sla_resolve_hours": rule["resolve_hours"],
        "response_deadline": now + timedelta(hours=rule["response_hours"]),
        "resolve_deadline": now + timedelta(hours=rule["resolve_hours"]),
    }


def check_overdue(ticket: object) -> bool:
    now = datetime.now(timezone.utc)
    if ticket.response_deadline and ticket.status in (1, 2) and now > ticket.response_deadline:
        return True
    if ticket.resolve_deadline and ticket.status != 4 and now > ticket.resolve_deadline:
        return True
    return False
