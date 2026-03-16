"at the top of the code"
import json

"with editable varibles"
LEADERBOARD_PATH = "leaderboard.json" # File name for the leaderboard (has to have ".json" at the end)
leaderboard_lenth = 10 # lenth of leader board displayed

"with functions"
def _ensure_file():
    """Create leaderboard file if it does not exist."""
    try:
        with open(LEADERBOARD_PATH, "r"):
            pass
    except:
        with open(LEADERBOARD_PATH, "w") as f:
            f.write("[]")


def _load():
    """Load leaderboard entries from file."""
    _ensure_file()
    try:
        with open(LEADERBOARD_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def _save(entries):
    """Save leaderboard entries to file."""
    with open(LEADERBOARD_PATH, "w") as f:
        json.dump(entries, f)

def record_result(name, rounds):
    """
    Store or update player score.
    Only highest score per player is kept.
    Zero-round games are ignored.
    If multiple players have the same score,
    the order is based on when they achieved it.
    """
    if rounds == 0:
        return

    entries = _load()
    found = False

    for entry in entries:
        if entry["player_name"] == name:
            # Only update if new score is higher
            if rounds > entry["rounds"]:
                entry["rounds"] = rounds
            found = True
            break

    if not found:
        entries.append({
            "player_name": name,
            "rounds": rounds
        })

    # Stable sort: highest score first.
    # Equal scores keep original insertion order.
    entries.sort(key=lambda x: x["rounds"], reverse=True)

    _save(entries)
    
def print_leaderboard():
    """Print top scores to serial console."""
    entries = _load()
    entries.sort(key=lambda x: x["rounds"], reverse=True)

    print("\n=== Leaderboard ===")
    for i, entry in enumerate(entries[:leaderboard_lenth], 1):
        print(f"{i}) {entry['player_name']} - {entry['rounds']} rounds")
