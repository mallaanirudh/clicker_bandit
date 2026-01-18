import streamlit as st

from app.state import ensure_state
from app.instructor import render_instructor_panel
from app.student import render_student_panel
from app.visuals import render_visuals


# ----------------------------
# App Configuration
# ----------------------------
st.set_page_config(
    page_title="Classroom Clicker Bandit",
    page_icon="🎰",
    layout="wide",
)


# ----------------------------
# Main App
# ----------------------------

def main():
    ensure_state()

    st.title("🎰 Classroom Clicker Bandit")
    st.caption("Make decisions. No hints. Maximize your reward.")

    # Layout: Instructor | Student | Results
    col_instructor, col_student, col_results = st.columns([1, 2, 2])

    with col_instructor:
        render_instructor_panel()

    with col_student:
        render_student_panel()

    with col_results:
        render_visuals()


if __name__ == "__main__":
    main()
