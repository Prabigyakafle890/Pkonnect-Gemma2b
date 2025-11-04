def check_user_type(email):
    if email.endswith("@pkcampus.edu.np"):
        return "institutional"
    return "guest"
