import numpy as np


def energy(J, s):
    return -0.5 * np.dot(s.T, np.dot(J, s))


def hopfield_gibbs_sampling(L, n, p, total_steps=5000 * 100, store_interval=500, burn_in_steps=450000):
    """
    Run Gibbs sampling on a Hopfield network and return the sampled states.

    Parameters:
    - L: int, sequence length.
    - n: int, number of patterns.
    - p: float, probability of x_i = 1 in the patterns.
    - total_steps: int, total number of Gibbs sampling steps (default is 5000 * 100).
    - store_interval: int, interval for storing the states (default is 500).
    - burn_in_steps: int, number of steps before starting to store states (default is 50000).

    Returns:
    - sset: numpy array of shape (L, num_stored_steps), the stored states.
    """
    # Generate binary patterns
    x = np.random.uniform(0, 1, (n, L))
    patterns = np.where(x > p, 1, -1)

    # Compute weight matrix using Hebbian learning rule
    J = 1 / L * np.dot(patterns.T, patterns)
    np.fill_diagonal(J, 0)

    # Initial state
    s = np.random.uniform(0, 1, L)
    s = np.where(s > p, 1, -1)

    # Number of steps to store
    num_stored_steps = (total_steps - burn_in_steps) // store_interval

    # Array to store the states
    sset = np.zeros((L, num_stored_steps))
    Eset = np.zeros(num_stored_steps)
    # Gibbs sampling
    for t in range(total_steps):
        ind = np.random.randint(0, L)
        r = np.random.uniform(0, 1)
        p_up = 1 / (1 + np.exp(-2 * np.dot(J[:, ind], s)))
        s[ind] = 1 if p_up > r else -1

        # Store the state every 'store_interval' steps after burn-in
        if t >= burn_in_steps and (t + 1) % store_interval == 0:
            store_index = (t - burn_in_steps) // store_interval
            sset[:, store_index] = s
            Eset[store_index] = energy(J, s)

        # # Print progress every 5000 steps
        # if (t + 1) % 5000 == 0 or t == 0:
        #     print(f"Iteration {t + 1} / {total_steps} ({(t + 1) / total_steps * 100:.2f}%)")

    return sset, Eset, patterns