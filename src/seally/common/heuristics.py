import numpy as np

from seally.env.environment import Position


def euclidean_distance(source: Position, goal: Position) -> float:
    """
    Computes the Euclidean distance between the source and goal positions.

    Args:
        source: The source position.
        goal: The goal position.

    Returns:
        The Euclidean distance between the source and goal positions.
    """
    return float(np.linalg.norm(source.dim_array - goal.dim_array))

def manhattan_distance(source: Position, goal: Position) -> float:
    """
    Computes the Manhattan distance between the source and goal positions.

    Args:
        source: The source position.
        goal: The goal position.

    Returns:
        The Manhattan distance between the source and goal positions.
    """
    return float(np.sum(np.abs(source.dim_array - goal.dim_array)))

def chebyshev_distance(source: Position, goal: Position) -> float:
    """
    Computes the Chebyshev distance between the source and goal positions.

    Args:
        source: The source position.
        goal: The goal position.

    Returns:
        The Chebyshev distance between the source and goal positions.
    """
    return float(np.linalg.norm(source.dim_array - goal.dim_array, ord=np.inf))