from typing import Dict, List, Optional
from seally.common.path import Path
from seally.env.environment import Environment, Position

class DFS():
    """
    Depth First Search algorithm for finding paths between points in an environment.
    """
    def __init__(self, env: Environment):
        """
        Initialize a DFS Object.

        Args:
            env: An Environment to search.
        """
        self.env = env

    def compute_path(self, source: Position, goal: Position) -> Path:
        """
        Computes a path from the source position to the goal position using the Depth First Search Algorithm.

        Args:
            source: The source position in the environment.
            goal: The goal position in the environment.

        Returns:
            A path from source to goal.
        """

        if not self.env.in_bounds(source) or self.env.is_occupied(source):
            raise Exception("Source is not a valid position")
        
        if not self.env.in_bounds(goal) or self.env.is_occupied(goal):
            raise Exception("Goal is not a valid position")

        open_set = [source]
        visited = {source}
        came_from: Dict[Position, Optional[Position]] = {source: None}

        current = source
        while open_set:
            current = open_set.pop()

            if current == goal:
                break

            for next_cell in self.env.get_neighbors(current):
                if self.env.is_occupied(next_cell) or next_cell in visited:
                    continue
                visited.add(next_cell)
                came_from[next_cell] = current
                open_set.append(next_cell)

        if current != goal:
            raise Exception("Path not found")

        path: List[Position] = []
        trace: Optional[Position] = goal
        while trace is not None:
            path.append(trace)
            trace = came_from.get(trace)
        path.reverse()
        return path
