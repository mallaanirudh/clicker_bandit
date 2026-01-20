import streamlit as st
import uuid

from core.environment import BanditEnvironment
from core.bandit_agent import ThompsonSamplingAgent
from core.metrics import MetricsTracker

# ----------------------------
# Session Configuration (LOCKED)
# ----------------------------
K_ARMS = 5
MAX_PULLS = 35
ENV_SEED = 42
AGENT_SEED = 123


# ----------------------------
# Initialization Helpers
# ----------------------------

def _init_environment():
    return BanditEnvironment(k=K_ARMS, seed=ENV_SEED)

def _init_agent():
    return ThompsonSamplingAgent(k=K_ARMS, seed=AGENT_SEED)

def _init_metrics(env: BanditEnvironment):
    human = MetricsTracker(k=K_ARMS, optimal_prob=env.optimal_prob)
    agent = MetricsTracker(k=K_ARMS, optimal_prob=env.optimal_prob)
    return human, agent


# ----------------------------
# State Bootstrap
# ----------------------------

def ensure_state():
    ss = st.session_state

    if "initialized" not in ss:
        ss.initialized = True

        ss.user_id = str(uuid.uuid4())[:8]
        ss.user_name = f"Player {ss.user_id}"  # Default name
        ss.score_submitted = False

        ss.session_active = False
        ss.reveal_phase = False

        ss.env = _init_environment()
        ss.agent = _init_agent()
        ss.human_metrics, ss.agent_metrics = _init_metrics(ss.env)

        ss.remaining_pulls = MAX_PULLS


# ----------------------------
# Session Control
# ----------------------------

def start_session():
    ss = st.session_state

    ss.session_active = True
    ss.reveal_phase = False
    ss.score_submitted = False

    ss.env = _init_environment()
    ss.agent = _init_agent()
    ss.human_metrics, ss.agent_metrics = _init_metrics(ss.env)

    ss.remaining_pulls = MAX_PULLS


def end_session():
    ss = st.session_state

    ss.session_active = False
    ss.reveal_phase = True

    finalize_session()
    st.rerun()


def finalize_session():
    ss = st.session_state

    if ss.score_submitted:
        return

    from app.leaderboard import submit_score

    submit_score(ss.user_id, ss.human_metrics.total_reward, ss.user_name)
    ss.score_submitted = True


# ----------------------------
# Gameplay
# ----------------------------

def can_pull() -> bool:
    ss = st.session_state
    return ss.session_active and ss.remaining_pulls > 0


def step(human_arm: int):
    ss = st.session_state

    if not can_pull():
        return

    # consume pull FIRST
    ss.remaining_pulls -= 1

    # --- Human ---
    human_reward = ss.env.pull(human_arm)
    ss.human_metrics.update(human_arm, human_reward)

    # --- Agent ---
    agent_arm = ss.agent.select_arm()
    agent_reward = ss.env.pull(agent_arm)
    ss.agent.update(agent_arm, agent_reward)
    ss.agent_metrics.update(agent_arm, agent_reward)

    if ss.remaining_pulls == 0:
        end_session()


# ----------------------------
# Reveal
# ----------------------------

def reveal_environment():
    ss = st.session_state
    if not ss.reveal_phase:
        return None
    return ss.env.reveal()
