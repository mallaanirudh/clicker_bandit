import numpy as np

class BanditEnvironment:
    """
    Shared stationary k-armed bandit with optional deceptive early bias.
    This class is the single source of truth for reward generation.
    Agents and humans NEVER see true probabilities during play.
    """

    def __init__(
        self,
        k: int = 5,
        seed: int = 42,
        true_probs=None,
        bias_arm: int | None = 1,
        bias_prob: float = 0.9,
        bias_pulls: int = 5,
    ):
        """
        Parameters
        ----------
        k : int
            Number of arms
        seed : int
            RNG seed to ensure identical distributions across users
        true_probs : list[float] | None
            True Bernoulli probabilities for each arm
        bias_arm : int | None
            Arm index to receive deceptive early bias (None disables bias)
        bias_prob : float
            Temporary probability during biased phase
        bias_pulls : int
            Number of initial pulls during which bias applies
        """

        self.k = k
        self.rng = np.random.default_rng(seed)

        if true_probs is None:
            # Asymmetric, fast-learning distribution (LOCKED DESIGN)
            self.true_probs = np.array([0.80, 0.65, 0.50, 0.30, 0.10])
        else:
            self.true_probs = np.array(true_probs, dtype=float)

        assert len(self.true_probs) == self.k, "Probability vector size mismatch"

        self.optimal_arm = int(np.argmax(self.true_probs))
        self.optimal_prob = float(np.max(self.true_probs))

        # Deceptive bias configuration
        self.bias_arm = bias_arm
        self.bias_prob = bias_prob
        self.bias_pulls = bias_pulls

        self.total_pulls = 0

    def pull(self, arm: int) -> int:
        """
        Pull an arm and receive a Bernoulli reward.
        Bias is applied only during the initial bias_pulls.
        """
        assert 0 <= arm < self.k, "Invalid arm index"

        self.total_pulls += 1

        # Apply deceptive early bias if active
        if (
            self.bias_arm is not None
            and arm == self.bias_arm
            and self.total_pulls <= self.bias_pulls
        ):
            prob = self.bias_prob
        else:
            prob = self.true_probs[arm]

        reward = 1 if self.rng.random() < prob else 0
        return reward

    def regret(self, reward: int) -> float:
        """
        Instantaneous regret relative to optimal arm.
        """
        return self.optimal_prob - reward

    def reveal(self) -> dict:
        """
        Reveal true environment parameters AFTER the session ends.
        """
        return {
            "true_probs": self.true_probs.copy(),
            "optimal_arm": self.optimal_arm,
            "optimal_prob": self.optimal_prob,
            "bias_arm": self.bias_arm,
            "bias_prob": self.bias_prob,
            "bias_pulls": self.bias_pulls,
        }
