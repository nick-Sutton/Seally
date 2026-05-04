from collections import deque
from typing import List, Optional
from seally.common.path import Path
from seally.env.environment import Environment, Position

class FlowField():
    """
    Flow Field algorithm for finding paths between points in an environment.
    """

    def __init__(self, env: Environment):
        """
        Initialize a FlowField Object.

        Args:
            env: An Environment to search.
        """
        self.env = env
        self._field: dict[Position, Position] = {}
        self._goal: Optional[Position] = None

    def compute_field(self, goal: Position) -> None:
        """
        Builds a flow field across the entire environment pointing toward goal.
        Uses reverse BFS from the goal so every reachable cell gets a direction.

        Args:
            goal: The goal position all agents should move toward.
        """
        if not self.env.in_bounds(goal) or self.env.is_occupied(goal):
            raise Exception("Goal is not a valid position")

        self._goal = goal
        self._field = {}

        came_from: dict[Position, Optional[Position]] = {goal: None}
        open_set = deque([goal])

        while open_set:
            current = open_set.popleft()
            for neighbor in self.env.get_neighbors(current):
                if self.env.is_occupied(neighbor) or neighbor in came_from:
                    continue

                came_from[neighbor] = current
                open_set.append(neighbor)

        # Each cell points towards the next cell in the direction of the goal
        for cell, next_step in came_from.items():
            if next_step is not None:          # goal cell has no direction
                self._field[cell] = next_step

    def compute_path(self, source: Position, goal: Position) -> Path:
        """
        Returns a path from source to goal using the flow field.
        Recomputes the field if the goal has changed.
        
        Args:
            source: The source position in the environment.
            goal:   The goal position in the environment.
        Returns:
            A path from source to goal.
        """
        if not self.env.in_bounds(source) or self.env.is_occupied(source):
            raise Exception("Source is not a valid position")

        # Only recompute the field when the goal changes
        if goal != self._goal:
            self.compute_field(goal)

        if source not in self._field and source != goal:
            raise Exception("Path not found")

        # Walk the field from source to goal
        path: List[Position] = [source]
        current = source
        while current != goal:
            current = self._field[current]
            path.append(current)

        return path
