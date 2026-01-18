import streamlit as st

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
# State Initialization Helpers
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
# Public State API
# ----------------------------

def ensure_state():
    """
    Ensure all required session state variables exist.
    Safe to call on every Streamlit rerun.
    """
    ss = st.session_state

    if "initialized" not in ss:
        ss.initialized = True

        ss.session_active = False
        ss.reveal_phase = False

        ss.env = _init_environment()
        ss.agent = _init_agent()
        ss.human_metrics, ss.agent_metrics = _init_metrics(ss.env)

        ss.remaining_pulls = MAX_PULLS


def start_session():
    """
    Start (or restart) a fresh session.
    This wipes all prior state deterministically.
    """
    ss = st.session_state

    ss.session_active = True
    ss.reveal_phase = False

    ss.env = _init_environment()
    ss.agent = _init_agent()
    ss.human_metrics, ss.agent_metrics = _init_metrics(ss.env)

    ss.remaining_pulls = MAX_PULLS


def end_session():
    """
    End the active session and enter reveal phase.
    """
    ss = st.session_state
    ss.session_active = False
    ss.reveal_phase = True


def can_pull() -> bool:
    """
    Check whether the human is allowed to pull another arm.
    """
    ss = st.session_state
    return ss.session_active and ss.remaining_pulls > 0


def step(human_arm: int):
    """
    Execute one timestep:
    - Human pulls chosen arm
    - Agent pulls its selected arm
    - Environment generates rewards
    - Metrics update
    - Remaining pulls decremented
    """
    ss = st.session_state

    if not can_pull():
        return

    # --- Human step ---
    human_reward = ss.env.pull(human_arm)
    ss.human_metrics.update(human_arm, human_reward)

    # --- Agent step ---
    agent_arm = ss.agent.select_arm()
    agent_reward = ss.env.pull(agent_arm)
    ss.agent.update(agent_arm, agent_reward)
    ss.agent_metrics.update(agent_arm, agent_reward)

    # --- Bookkeeping ---
    ss.remaining_pulls -= 1

    if ss.remaining_pulls <= 0:
        end_session()


def reveal_environment():
    """
    Reveal true environment parameters (only valid after session ends).
    """
    ss = st.session_state
    if not ss.reveal_phase:
        return None
    return ss.env.reveal()
