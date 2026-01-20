import streamlit as st

@st.cache_resource
def get_leaderboard():
    """
    Shared leaderboard across all Streamlit sessions.
    Resets only when app restarts.
    """
    return {}

def submit_score(user_id: str, total_reward: int, user_name: str):
    """
    Submit score exactly once per user.
    """
    leaderboard = get_leaderboard()

    # Prevent overwrite / duplicate submission
    if user_id in leaderboard:
        return

    leaderboard[user_id] = {
        "score": total_reward,
        "name": user_name
    }

def get_sorted_leaderboard():
    """
    Return leaderboard sorted by score descending.
    """
    leaderboard = get_leaderboard()

    # Handle both old (int) and new (dict) formats for backward compatibility
    # during user transition if any persistence existed (though it's in-memory)
    # But since it is in-memory, we can assume new format after restart.
    
    # However, to be safe against hot-reload issues:
    formatted_data = []
    for uid, data in leaderboard.items():
        if isinstance(data, int):
            # Fallback for old data
            formatted_data.append({"User": uid, "Score": data})
        else:
            formatted_data.append({"User": data["name"], "Score": data["score"]})

    return sorted(
        formatted_data,
        key=lambda x: x["Score"],
        reverse=True
    )
