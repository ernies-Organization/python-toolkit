def check_password_strength(password):
    score = 0
    length = len(password)

    # --- length scoring ---
    if length >= 16:
        score += 4
    elif length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    elif length >= 6:
        score += 1

    # --- character type checks ---
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 2

    # --- pattern penalties ---
    if password.isalpha() or password.isdigit():
        score -= 2

    if len(set(password)) == 1:
        score -= 3

    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            score -= 1
            break

    sequences = ["abc", "123", "qwerty", "asdf"]
    lower_pw = password.lower()
    if any(seq in lower_pw for seq in sequences):
        score -= 2

    # --- clamp score ---
    if score < 0:
        score = 0

    # --- strength label ---
    if score <= 2:
        strength = "Very Weak"
    elif score <= 4:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    elif score <= 8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return strength, score

"test"
# you dont need this in the code only to try it out


password = input("what is the password you want to check?")
strength, score = check_password_strength(password)
print(f"your password strength is {strength}, your score is {score}")
