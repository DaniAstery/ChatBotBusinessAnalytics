logs = []

def log_message(user, message, response_type):
    logs.append({
        "user": user,
        "message": message,
        "type": response_type
    })

    print("LOG:", logs[-1])