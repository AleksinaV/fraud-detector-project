import numpy as np
from scipy.optimize import differential_evolution


def weighted_difference(text1_params, text2_params, weights, total_words1, total_words2):
    """
    Calculate the weighted difference between two texts.

    Args:
    text1_params (list or np.array): Parameters of the first text.
    text2_params (list or np.array): Parameters of the second text.
    weights (list or np.array): Weights for each parameter.
    total_words1 (int): Total number of words in the first text.
    total_words2 (int): Total number of words in the second text.

    Returns:
    float: The weighted difference between the two texts.
    """
    text1_params = np.array(text1_params)
    text2_params = np.array(text2_params)
    weights = np.array(weights)

    # Calculate the weighted differences
    weighted_diffs = weights * (text1_params - text2_params)

    # Normalize by the total number of words in the texts
    normalized_diff = np.sum(np.abs(weighted_diffs)) / (total_words1 + total_words2)

    return -normalized_diff  # Negate because we will be minimizing in the optimization function


def objective_with_regularization(weights, text1_params, text2_params, total_words1, total_words2, alpha=0.01):
    """
    Objective function with L2 regularization.

    Args:
    weights (list or np.array): Weights for each parameter.
    text1_params (list or np.array): Parameters of the first text.
    text2_params (list or np.array): Parameters of the second text.
    total_words1 (int): Total number of words in the first text.
    total_words2 (int): Total number of words in the second text.
    alpha (float): Regularization strength.

    Returns:
    float: Regularized objective value.
    """
    diff = weighted_difference(text1_params, text2_params, weights, total_words1, total_words2)
    l2_penalty = alpha * np.sum(weights ** 2)
    return diff + l2_penalty


def optimize_weights(text1_params, text2_params, total_words1, total_words2, alpha=0.01):
    """
    Optimize weights to maximize the weighted difference between two texts.

    Args:
    text1_params (list or np.array): Parameters of the first text.
    text2_params (list or np.array): Parameters of the second text.
    total_words1 (int): Total number of words in the first text.
    total_words2 (int): Total number of words in the second text.
    alpha (float): Regularization strength.

    Returns:
    list: Optimal weights for maximizing the weighted difference.
    """
    # Define the bounds for the weights (e.g., between 0 and 5)
    bounds = [(0, 5) for _ in range(len(text1_params))]

    # Define the objective function for optimization with regularization
    def objective(weights):
        return objective_with_regularization(weights, text1_params, text2_params, total_words1, total_words2, alpha)

    # Perform the optimization using differential evolution
    result = differential_evolution(objective, bounds)

    return result.x


def calculate_weight(text1_params, text1_word_count, text2_params, text2_word_count):
    # Regularization strength
    alpha = 0.01

    optimal_weights = optimize_weights(text1_params, text2_params, text1_word_count, text2_word_count, alpha)
    print(f"Optimal weights: {optimal_weights}")

    # Calculate the maximized difference using the optimal weights
    max_diff = -weighted_difference(text1_params, text2_params, optimal_weights, text1_word_count, text2_word_count)
    print(f"Maximized difference between texts: {max_diff}")

    return optimal_weights
