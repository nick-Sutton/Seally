import numpy as np

from src.seally.env.enviroment import Position


def euclidean_distance(source: Position, goal: Position) -> float:
    """
    Computes the Euclidean distance between the source and goal GridCells.

    Args:
        source: The source cell.
        goal: The goal cell.

    Returns:
        The Euclidean distance between the source and goal GridCells.
    """
    return float(np.linalg.norm(source.dim_array - goal.dim_array))

def manhattan_distance(source: Position, goal: Position) -> float:
    """
    Computes the Manhattan distance between the source and goal GridCells.

    Args:
        source: The source cell.
        goal: The goal cell.

    Returns:
        The Manhattan distance between the source and goal GridCells.
    """
    return float(np.sum(np.abs(source.dim_array - source.dim_array)))

def chebyshev_distance(source: Position, goal: Position) -> float:
    """
    Computes the Chebyshev distance between the source and goal GridCells.

    Args:
        source: The source cell.
        goal: The goal cell.

    Returns:
        The Chebyshev distance between the source and goal GridCells.
    """
    return float(np.linalg.norm(source.dim_array - goal.dim_array, ord=np.inf))