import streamlit as st
from app.state import ensure_state, start_session, end_session


def render_instructor_panel():
    """
    Render instructor controls:
    - Start / reset session
    - Force end session
    - Reveal status
    """
    ensure_state()
    ss = st.session_state

    st.subheader("🎓 Instructor Controls")

    # Session control buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start / Reset Session"):
            start_session()
            st.success("Session started. Students may begin.")

    with col2:
        if st.button("⏹ End Session", disabled=not ss.session_active):
            end_session()
            st.warning("Session ended manually.")

    # ----------------------------
    # Danger Zone
    # ----------------------------
    st.markdown("---")
    with st.expander("☠️ Danger Zone"):
        st.caption("Reset the leaderboard. This cannot be undone.")
        
        from app.leaderboard import reset_leaderboard
        
        password = st.text_input("Admin Password", type="password")
        
        if st.button("Reset Leaderboard"):
            if password == "admin123":
                reset_leaderboard()
                st.success("Leaderboard wiped successfully!")
                st.rerun()
            else:
                st.error("Incorrect password!")

    # Status indicators
    st.markdown("---")

    if ss.session_active:
        st.info("🟢 Session ACTIVE")
        st.write(f"Remaining pulls per student: **{ss.remaining_pulls}**")
    elif ss.reveal_phase:
        st.success("🟣 Reveal phase")
    else:
        st.info("⚪ Session not started")
