from collections.abc import Callable
import heapq
from typing import Dict, List, Optional, Tuple
from seally.common.path import Path
from seally.env.environment import Environment, Position

class AStar():
    """
    A* Algorithm for finding the shortest path between points in an environment.
    """
    def __init__(self, env: Environment, heuristic: Callable[[Position, Position], float]):
        """
        Initialize an A* Object.

        Args:
            env: An Environment to Search.
            heuristic: The "Cost to Go" heuristic. 
        """
        self.env = env
        self.heuristic = heuristic

    def compute_path(self, source: Position, goal: Position) -> Path:
        """
        Computes the shortest path from the source position to the goal position using the A* Algorithm.

        Args:
            source: The source position in the environment.
            goal: The goal position in the environment.

        Returns:
            The shortest path from source to goal.
        """

        if not self.env.in_bounds(source) or self.env.is_occupied(source):
            raise Exception("Source is not a valid position")
        
        if not self.env.in_bounds(goal) or self.env.is_occupied(goal):
            raise Exception("Goal is not a valid position")

        tie_count = 0
        open_set: List[Tuple[float, int, Position]] = []
        heapq.heappush(open_set, (0.0, tie_count, source))

        came_from: Dict[Position, Optional[Position]] = {source: None}
        cost_so_far: Dict[Position, float] = {source: 0.0}
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

                new_cost = cost_so_far[current] + self.env.get_cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
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
