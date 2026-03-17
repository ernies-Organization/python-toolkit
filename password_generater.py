import secrets

# character groups
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits    = "0123456789"
symbols   = "!@#$%^&*()-_=+[]{};:,.<>?/\\"

groups = [lowercase, uppercase, digits, symbols]


def ask_yes_no(prompt):
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please enter y or n.")


def generate_password():
    # select groups
    while True:
        enabled = [
            ask_yes_no("Include lowercase letters?"),
            ask_yes_no("Include uppercase letters?"),
            ask_yes_no("Include digits?"),
            ask_yes_no("Include symbols?")
        ]
        if any(enabled):
            break
        print("You must select at least one group.\n")

    selected_groups = [groups[i] for i in range(4) if enabled[i]]
    all_chars = [c for g in selected_groups for c in g]

    # length input
    while True:
        length_input = input("Password length: ")
        if length_input.isdigit():
            length = int(length_input)
            if length >= len(selected_groups):
                break
            print(f"Length must be at least {len(selected_groups)}.")
        else:
            print("Not a number.")

    # guarantee one from each group
    password_chars = [secrets.choice(g) for g in selected_groups]

    # fill remaining
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(all_chars))

    # shuffle securely
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)

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

# --- run ---
password = generate_password()
strength, score = check_password_strength(password)

print("\nYour password is:", password)
print("Password strength:", strength, f"(score: {score})")
