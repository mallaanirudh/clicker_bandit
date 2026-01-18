import numpy as np

class ThompsonSamplingAgent:
    """
    Thompson Sampling agent for Bernoulli bandits.
    This agent acts as the silent algorithmic benchmark.
    """

    def __init__(self, k: int, seed: int = 123):
        self.k = k
        self.rng = np.random.default_rng(seed)

        # Beta prior parameters for each arm
        self.alpha = np.ones(k)  # successes + 1
        self.beta = np.ones(k)   # failures + 1

        self.counts = np.zeros(k, dtype=int)
        self.total_reward = 0
        self.total_pulls = 0

    def select_arm(self) -> int:
        """
        Sample from each arm's posterior and select the max.
        """
        samples = self.rng.beta(self.alpha, self.beta)
        return int(np.argmax(samples))

    def update(self, arm: int, reward: int):
        """
        Update posterior after observing reward.
        """
        self.total_pulls += 1
        self.counts[arm] += 1
        self.total_reward += reward

        if reward == 1:
            self.alpha[arm] += 1
        else:
            self.beta[arm] += 1

    def reset(self):
        """
        Reset agent state (useful for new sessions).
        """
        self.alpha[:] = 1
        self.beta[:] = 1
        self.counts[:] = 0
        self.total_reward = 0
        self.total_pulls = 0
