import numpy as np

class MetricsTracker:
    """
    Tracks rewards, pulls, and regret for a single player (human or agent).
    This is deliberately dumb bookkeeping — no strategy logic lives here.
    """

    def __init__(self, k: int, optimal_prob: float):
        self.k = k
        self.optimal_prob = optimal_prob

        self.pulls = np.zeros(k, dtype=int)
        self.rewards = []            # reward at each timestep
        self.regrets = []            # instantaneous regret
        self.cumulative_regret = []  # running sum

        self.total_reward = 0

    def update(self, arm: int, reward: int):
        """
        Update metrics after a pull.
        """
        self.pulls[arm] += 1
        self.rewards.append(reward)

        regret = self.optimal_prob - reward
        self.regrets.append(regret)

        if not self.cumulative_regret:
            self.cumulative_regret.append(regret)
        else:
            self.cumulative_regret.append(self.cumulative_regret[-1] + regret)

        self.total_reward += reward

    def average_reward(self) -> float:
        if not self.rewards:
            return 0.0
        return float(np.mean(self.rewards))

    def total_pulls(self) -> int:
        return int(len(self.rewards))

    def summary(self) -> dict:
        """
        Compact summary for leaderboards / comparison.
        """
        return {
            "total_reward": int(self.total_reward),
            "average_reward": self.average_reward(),
            "total_pulls": self.total_pulls(),
            "pulls_per_arm": self.pulls.copy(),
            "final_regret": float(self.cumulative_regret[-1]) if self.cumulative_regret else 0.0,
        }

    def reset(self):
        self.pulls[:] = 0
        self.rewards.clear()
        self.regrets.clear()
        self.cumulative_regret.clear()
        self.total_reward = 0
