from collections.abc import Callable
import heapq
from typing import Dict, List, Optional, Tuple
from seally.common.path import Path
from seally.env.environment import Environment, Position

class GreedyBestFirst():
    """
    Greedy Best First Search algorithm for finding paths between points in an environment.
    """
    def __init__(self, env: Environment, heuristic: Callable[[Position, Position], float]):
        """
        Initialize a GBF Object.

        Args:
            env: An Enviroment to search.
            heuristic: The "Cost to Go" heuristic. 
        """
        self.env = env
        self.heuristic = heuristic

    def compute_path(self, source: Position, goal: Position) -> Path:
        """
        Computes a path from the source position to the goal position using the Greedy Best First Search Algorithm.

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

        tie_count = 0
        open_set: List[Tuple[float, int, Position]] = []
        heapq.heappush(open_set, (0.0, tie_count, source))

        came_from: Dict[Position, Optional[Position]] = {source: None}
        closed_set = set()  # track fully explored cells

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current in closed_set:  # already explored optimally, skip
                continue

            closed_set.add(current)

            if current == goal:
                break

            for next in self.env.get_neighbors(current):
                if self.env.is_occupied(next) or next in closed_set:
                    continue

                if next not in came_from:
                    priority = self.heuristic(next, goal)
                    tie_count += 1

                    heapq.heappush(open_set, (priority, tie_count, next))
                    came_from[next] = current

        if current != goal:
            raise Exception("Path not found")

        path: List[Position] = []
        trace: Optional[Position] = goal
        while trace is not None:
            path.append(trace)
            trace = came_from.get(trace)
        path.reverse()
        return path
