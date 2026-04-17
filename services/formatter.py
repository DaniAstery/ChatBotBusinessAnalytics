from datetime import datetime

def format_response(reply, response_type):
    return {
        "status": "success",
        "type": response_type,
        "reply": reply,
        "timestamp": datetime.utcnow().isoformat()
    }