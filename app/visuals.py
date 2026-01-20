import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from app.state import ensure_state, reveal_environment
from app.leaderboard import get_sorted_leaderboard


def render_visuals():
    ensure_state()
    ss = st.session_state

    # Single source of truth
    if not ss.reveal_phase or ss.remaining_pulls != 0:
        st.info("Results will appear here once the session ends.")
        return

    st.header("📊 Results & Reveal")

    # ----------------------------
    # Environment reveal
    # ----------------------------
    env_info = reveal_environment()
    true_probs = env_info["true_probs"]
    optimal_arm = env_info["optimal_arm"]

    st.subheader("🎯 True Arm Probabilities")

    fig, ax = plt.subplots()
    ax.bar(range(len(true_probs)), true_probs)
    ax.axhline(true_probs[optimal_arm], linestyle="--")
    ax.set_xlabel("Arm")
    ax.set_ylabel("Reward Probability")
    ax.set_title("Hidden Reward Distributions")
    st.pyplot(fig)

    # ----------------------------
    # Reward comparison
    # ----------------------------
    st.subheader("🏆 You vs Thompson Sampling")

    fig, ax = plt.subplots()
    ax.bar(
        ["Human", "Agent"],
        [ss.human_metrics.total_reward, ss.agent_metrics.total_reward]
    )
    ax.set_ylabel("Total Reward")
    ax.set_title("Total Reward Comparison")
    st.pyplot(fig)

    # ----------------------------
    # Arm usage
    # ----------------------------
    st.subheader("🧠 Arm Selection Behavior")

    x = np.arange(len(true_probs))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width / 2, ss.human_metrics.pulls, width, label="Human")
    ax.bar(x + width / 2, ss.agent_metrics.pulls, width, label="Agent")

    ax.set_xlabel("Arm")
    ax.set_ylabel("Number of Pulls")
    ax.set_title("Arm Usage Comparison")
    ax.legend()
    st.pyplot(fig)

    # ----------------------------
    # Regret curves
    # ----------------------------
    st.subheader("📉 Cumulative Regret")

    fig, ax = plt.subplots()
    ax.plot(ss.human_metrics.cumulative_regret, label="Human")
    ax.plot(ss.agent_metrics.cumulative_regret, label="Agent")

    ax.set_xlabel("Pull")
    ax.set_ylabel("Cumulative Regret")
    ax.set_title("Regret Over Time")
    ax.legend()
    st.pyplot(fig)

    # ----------------------------
    # Leaderboard
    # ----------------------------
    st.subheader("🏆 Leaderboard (Final Scores)")

    leaderboard = get_sorted_leaderboard()

    if leaderboard:
        df = pd.DataFrame(leaderboard)
        df.index += 1
        st.table(df)
    else:
        st.info("Waiting for all players to finish…")
