from seally.env.grid_map import GridCell
import numpy as np

def euclidean_distance(source: GridCell, goal: GridCell) -> float:
    """
    Computes the Euclidean distance between the source and goal GridCells.

    Args:
        source: The source cell.
        goal: The goal cell.

    Returns:
        The Euclidean distance between the source and goal GridCells.
    """
    source_mat = np.array((source.x, source.y))
    goal_mat = np.array((goal.x, goal.y))

    dist = np.linalg.norm(source_mat - goal_mat)

    return dist

def manhattan_distance(source: GridCell, goal: GridCell) -> float:
    """
    Computes the Manhattan distance between the source and goal GridCells.

    Args:
        source: The source cell.
        goal: The goal cell.

    Returns:
        The Manhattan distance between the source and goal GridCells.
    """
    source_mat = np.array((source.x, source.y))
    goal_mat = np.array((goal.x, goal.y))

    dist = np.sum(np.abs(source_mat - goal_mat))

    return dist

def chebyshev_distance(source: GridCell, goal: GridCell) -> float:
    """
    Computes the Chebyshev distance between the source and goal GridCells.

    Args:
        source: The source cell.
        goal: The goal cell.

    Returns:
        The Chebyshev distance between the source and goal GridCells.
    """
    source_mat = np.array((source.x, source.y))
    goal_mat = np.array((goal.x, goal.y))

    dist = np.linalg.norm(source_mat - goal_mat, ord=np.inf)

    return dist







