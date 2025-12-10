# leaderboard_tool.py
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.txt"

def load_leaderboard():
    """Load leaderboard from file, return dict by mode"""
    if not os.path.exists(LEADERBOARD_FILE):
        return {"Easy": [], "Medium": [], "Hard": []}

    leaderboards = {"Easy": [], "Medium": [], "Hard": []}
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) >= 3:
                name, score, mode = parts[:3]
                ts = parts[3] if len(parts) > 3 else ""
                leaderboards[mode].append((name, int(score), mode, ts))
    # Sort by score descending
    for mode in leaderboards:
        leaderboards[mode].sort(key=lambda x: x[1], reverse=True)
    return leaderboards

def save_to_leaderboard(name, score, mode):
    """Append a new score to the leaderboard file"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LEADERBOARD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name} | {score} | {mode} | {ts}\n")
