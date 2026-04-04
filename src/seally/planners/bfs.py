from collections import deque
from typing import List, Optional
from seally.common.path import Path
from seally.env.enviroment import Enviroment, Position

class BFS():
    """
    Breadth First Search algorithm for finding paths between points in a enviroment.
    """
    def __init__(self, env: Enviroment):
        """
        Initialize a BFS Object.

        Args:
            env: An Enviroment to search.
        """
        self.env = env

    def compute_path(self, source: Position, goal: Position) -> Path:
        """
        Computes a path from the source position to the goal position using the Breadth First Search Algorithm.

        Args:
            source: The source position in the enviroment.
            goal: The goal position in the enviroment.

        Returns:
            A path from source to goal.
        """

        if not self.env.in_bounds(source) or self.env.is_occupied(source):
            raise Exception("Source is not a valid position")
        
        if not self.env.in_bounds(goal) or self.env.is_occupied(goal):
            raise Exception("Goal is not a valid position")

        open_set = deque([source])
        visited = {source}
        came_from: dict = {source: None}

        while open_set:
            current = open_set.popleft()
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
