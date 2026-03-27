from seally.common.grid_cell import GridCell
import numpy as np

def euclidean_distance(source: GridCell, goal: GridCell) -> float:
    source_mat = np.array((source.x, source.y))
    goal_mat = np.array((goal.x, goal.y))

    dist = np.linalg.norm(source_mat - goal_mat)

    return dist

def manhattan_distance(source: GridCell, goal: GridCell) -> float:
    source_mat = np.array((source.x, source.y))
    goal_mat = np.array((goal.x, goal.y))

    dist = np.sum(np.abs(source_mat - goal_mat))

    return dist

def chebyshev_distance(source: GridCell, goal: GridCell) -> float:
    source_mat = np.array((source.x, source.y))
    goal_mat = np.array((goal.x, goal.y))

    dist = np.linalg.norm(source_mat - goal_mat, ord=np.inf)

    return dist







