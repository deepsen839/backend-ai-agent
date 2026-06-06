KEYWORDS = [
    "enterprise",
    "starter",
    "growth",
    "pricing",
    "price",
    "sso",
    "audit logs",
    "sla",
    "webhooks"
]


def extract_memory_fact(
    message: str
):
    text = message.lower()

    found = []

    for keyword in KEYWORDS:
        if keyword in text:
            found.append(keyword)

    if not found:
        return None

    return (
        "User interested in: "
        + ", ".join(found)
    )