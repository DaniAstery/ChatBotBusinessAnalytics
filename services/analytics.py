stats = {
    "total_messages": 0,
    "sales": 0,
    "support": 0,
    "lead": 0,
    "ai": 0
}

def track_event(event_type):
    stats["total_messages"] += 1

    if event_type in stats:
        stats[event_type] += 1


def get_stats():
    return stats