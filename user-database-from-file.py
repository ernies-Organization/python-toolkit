# -----------------------------
# Account System With File Saving (JSON)
# - Login / Signup
# - First user becomes admin
# - Full admin control panel
# - Accounts stored in user_database.json
# -----------------------------

import json

# -----------------------------
# FILE SAVE / LOAD SYSTEM
# -----------------------------

DATABASE_PATH = "user_database.json"


def _ensure_db():
    """Create database file if missing."""
    try:
        with open(DATABASE_PATH, "r"):
            pass
    except:
        with open(DATABASE_PATH, "w") as f:
            f.write("[]")


def _load_users():
    """Load users from JSON file."""
    _ensure_db()
    try:
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def _save_users(user_list):
    """Save users to JSON file."""
    with open(DATABASE_PATH, "w") as f:
        json.dump(user_list, f, indent=4)


# -----------------------------
# GLOBALS
# -----------------------------

users = _load_users()
name = ""
password = ""
admin = False


# -----------------------------
# LOGIN / SIGNUP
# -----------------------------
def user_login():
    global name, password, admin

    if users == []:
        print("No users found. Creating first admin user...")
        create_user(True)
        return

    choice = input("Login or signup? (login/signup): ").strip().lower()

    if choice == "signup":
        create_user(False)
        return

    if choice == "login":
        name = input("Username: ").strip().lower()

        found = None
        for u in users:
            if u["username"] == name:
                found = u
                break

        if not found:
            print("User not found.")
            return user_login()

        password = input("Password: ").strip()

        if password == found["password"]:
            admin = found["admin"]
            print("Login successful!")
            info()
        else:
            print("Incorrect password.")
            user_login()
    else:
        print("Invalid input.")
        user_login()


# -----------------------------
# CREATE USER
# -----------------------------
def create_user(is_admin):
    global name, password, admin

    name = input("Choose username: ").strip().lower()

    for u in users:
        if u["username"] == name:
            print("Username already exists.")
            return create_user(is_admin)

    password = input("Choose password: ").strip()

    users.append({"username": name, "password": password, "admin": is_admin})
    _save_users(users)

    admin = is_admin
    print(f"User '{name}' created. Admin = {admin}")
    info()


# -----------------------------
# MAIN USER MENU
# -----------------------------
def info():
    if admin:
        choice = input(f"{name}, choose (admin/password/name/delete/logout): ").strip().lower()
    else:
        choice = input(f"{name}, choose (password/name/delete/logout): ").strip().lower()

    if choice == "admin" and admin:
        admin_info()
    elif choice == "password":
        change_password()
    elif choice == "name":
        change_name()
    elif choice == "delete":
        delete_account()
    elif choice == "logout":
        logout()
    else:
        print("Invalid option.")
        info()


# -----------------------------
# ADMIN MENU
# -----------------------------
def admin_info():
    choice = input(
        "\n--- ADMIN PANEL ---\n"
        "view_users\n"
        "delete_user\n"
        "promote_user\n"
        "demote_user\n"
        "reset_user_password\n"
        "change_user_name\n"
        "view_user_details\n"
        "create_user\n"
        "back\n> "
    ).strip().lower()

    if choice == "view_users":
        admin_view_users()
    elif choice == "delete_user":
        admin_delete_user()
    elif choice == "promote_user":
        admin_promote_user()
    elif choice == "demote_user":
        admin_demote_user()
    elif choice == "reset_user_password":
        admin_reset_user_password()
    elif choice == "change_user_name":
        admin_change_user_name()
    elif choice == "view_user_details":
        admin_view_user_details()
    elif choice == "create_user":
        admin_create_user()
    elif choice == "back":
        info()
    else:
        print("Invalid option.")
        admin_info()


# -----------------------------
# ADMIN FUNCTIONS
# -----------------------------
def admin_view_users():
    print("\n--- USERS ---")
    for i, u in enumerate(users, 1):
        role = "Admin" if u["admin"] else "User"
        print(f"{i}. {u['username']} ({role})")
    admin_info()


def admin_delete_user():
    target = input("Username to delete: ").strip().lower()

    if target == name:
        print("Admins cannot delete themselves.")
        return admin_info()

    for u in users:
        if u["username"] == target:
            if u["admin"] and sum(x["admin"] for x in users) <= 1:
                print("Cannot delete last admin.")
                return admin_info()

            users.remove(u)
            _save_users(users)
            print(f"User '{target}' deleted.")
            return admin_info()

    print("User not found.")
    admin_info()


def admin_promote_user():
    target = input("Username to promote: ").strip().lower()

    for u in users:
        if u["username"] == target:
            u["admin"] = True
            _save_users(users)
            print("User promoted.")
            return admin_info()

    print("User not found.")
    admin_info()


def admin_demote_user():
    target = input("Username to demote: ").strip().lower()

    for u in users:
        if u["username"] == target:
            if sum(x["admin"] for x in users) <= 1:
                print("Cannot demote last admin.")
                return admin_info()

            u["admin"] = False
            _save_users(users)
            print("User demoted.")
            return admin_info()

    print("User not found.")
    admin_info()


def admin_reset_user_password():
    target = input("Username: ").strip().lower()

    for u in users:
        if u["username"] == target:
            new = input("New password: ")
            u["password"] = new
            _save_users(users)
            print("Password reset.")
            return admin_info()

    print("User not found.")
    admin_info()


def admin_change_user_name():
    old = input("Current username: ").strip().lower()
    new = input("New username: ").strip().lower()

    for u in users:
        if u["username"] == new:
            print("Username already exists.")
            return admin_info()

    for u in users:
        if u["username"] == old:
            u["username"] = new
            _save_users(users)
            print("Username changed.")
            return admin_info()

    print("User not found.")
    admin_info()


def admin_view_user_details():
    target = input("Username: ").strip().lower()

    for u in users:
        if u["username"] == target:
            print("\n--- USER DETAILS ---")
            print(f"Username: {u['username']}")
            print(f"Password: {u['password']}")
            print(f"Admin: {u['admin']}")
            print("---------------------\n")
            return admin_info()

    print("User not found.")
    admin_info()


def admin_create_user():
    username = input("New username: ").strip().lower()

    for u in users:
        if u["username"] == username:
            print("Username exists.")
            return admin_info()

    password = input("Password: ").strip()
    is_admin = input("Make admin? (y/N): ").strip().lower() == "y"

    users.append({"username": username, "password": password, "admin": is_admin})
    _save_users(users)

    print("User created.")
    admin_info()


# -----------------------------
# NORMAL USER FUNCTIONS
# -----------------------------
def change_password():
    global password

    current = input("Current password: ").strip()
    if current != password:
        print("Incorrect password.")
        return info()

    new = input("New password: ").strip()
    password = new

    for u in users:
        if u["username"] == name:
            u["password"] = new

    _save_users(users)
    print("Password updated.")
    info()


def change_name():
    global name

    if input("Current username: ").strip().lower() != name:
        print("Incorrect username.")
        return info()

    new = input("New username: ").strip().lower()

    for u in users:
        if u["username"] == new:
            print("Username taken.")
            return info()

    for u in users:
        if u["username"] == name:
            u["username"] = new

    name = new
    _save_users(users)
    print("Username updated.")
    info()


def delete_account():
    global users

    if input("Type DELETE to confirm: ") != "DELETE":
        return info()

    users = [u for u in users if u["username"] != name]
    _save_users(users)

    print("Account deleted.")
    logout()


def logout():
    global name, password, admin

    name = ""
    password = ""
    admin = False

    user_login()


# -----------------------------
# START PROGRAM
# -----------------------------
user_login()
