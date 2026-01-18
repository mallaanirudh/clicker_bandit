import streamlit as st
from app.state import ensure_state, can_pull, step


def render_student_panel():
    """
    Render the student interaction panel:
    - Arm buttons
    - Remaining pulls
    - Immediate reward feedback
    """
    ensure_state()
    ss = st.session_state

    st.subheader("🎰 Choose an Arm")

    # Status display
    if ss.session_active:
        st.info(f"Remaining pulls: {ss.remaining_pulls}")
    elif ss.reveal_phase:
        st.warning("Session ended. Waiting for results reveal.")
    else:
        st.info("Session not started yet.")

    # Store last reward for feedback
    if "last_reward" not in ss:
        ss.last_reward = None

    # Disable buttons if cannot pull
    disabled = not can_pull()

    # Arm buttons
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            if st.button(f"Arm {i+1}", disabled=disabled):
                prev_pulls = ss.remaining_pulls
                step(i)

                # Infer reward from metrics update
                if ss.human_metrics.total_pulls() > 0:
                    ss.last_reward = ss.human_metrics.rewards[-1]

    # Immediate feedback
    if ss.last_reward is not None and ss.session_active:
        if ss.last_reward == 1:
            st.success("✅ Reward: 1")
        else:
            st.error("❌ Reward: 0")
