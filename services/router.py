def route_message(message: str):
    msg = message.lower()

    if any(x in msg for x in ["price", "cost", "how much", "buy", "plan", "subscription"]):
        return "sales"

    if any(x in msg for x in ["help", "error", "issue", "not working"]):
        return "support"

    if any(x in msg for x in ["contact", "demo", "service", "book"]):
        return "lead"

    return "ai"