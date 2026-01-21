import streamlit as st
import json
import os
import time

# Use absolute path to ensure we always find the file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level since app/ is a subdir
PROJECT_ROOT = os.path.dirname(BASE_DIR)
LEADERBOARD_FILE = os.path.join(PROJECT_ROOT, "leaderboard.json")

TTL_SECONDS = 15 * 60  # 15 minutes

def _load_leaderboard():
    """
    Load leaderboard data from JSON file.
    If file hasn't been modified in 15 mins, treat it as expired.
    """
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    
    # Check TTL
    try:
        mtime = os.path.getmtime(LEADERBOARD_FILE)
        if time.time() - mtime > TTL_SECONDS:
            # File is too old, ignore it (and effectively reset)
            return {}
            
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_leaderboard(data):
    """Save leaderboard data to JSON file."""
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError:
        st.error(f"Failed to save leaderboard to {LEADERBOARD_FILE}")

def submit_score(user_id: str, total_reward: int, user_name: str):
    """
    Submit score exactly once per user and persist to file.
    """
    leaderboard = _load_leaderboard()

    # Prevent overwrite / duplicate submission
    if user_id in leaderboard:
        return

    leaderboard[user_id] = {
        "score": total_reward,
        "name": user_name
    }
    
    _save_leaderboard(leaderboard)

def get_sorted_leaderboard():
    """
    Return leaderboard sorted by score descending.
    """
    leaderboard = _load_leaderboard()

    # Handle old/new format edge cases if necessary (though strictly new now)
    formatted_data = []
    for uid, data in leaderboard.items():
        if isinstance(data, int):
            formatted_data.append({"User": uid, "Score": data})
        else:
            formatted_data.append({"User": data["name"], "Score": data["score"]})

    return sorted(
        formatted_data,
        key=lambda x: x["Score"],
        reverse=True
    )

def reset_leaderboard():
    """Wipe all data from the leaderboard file."""
    _save_leaderboard({})
