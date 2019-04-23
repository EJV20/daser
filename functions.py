def signup_checks(nu, np):
    if nu < 8:
        return "Username not long enough"
    elif np < 8:
        return "Password not long enough"
    else:
        return 0
