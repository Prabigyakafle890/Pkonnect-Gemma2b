def recognize_intent(message):
    message = message.lower()
    if "admission" in message:
        return "admission_info"
    elif "result" in message:
        return "exam_result"
    elif "faculty salary" in message or "budget":
        return "confidential_finance"
    else:
        return "general"

def is_allowed_for_user(intent, user_type):
    restricted_intents = ["confidential_finance"]
    if intent in restricted_intents and user_type == "guest":
        return False
    return True
