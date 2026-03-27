from collections.abc import Callable
import heapq
import numpy as np
from seally.env.grid_map import GridMap, GridCell
from seally.common.path import Path

class AStar():
    def __init__(self, env: GridMap, heuristic: Callable[[GridCell, GridCell], float]):
        self.env = env
        self.heuristic = heuristic

    def cost(self, source: GridCell, goal: GridCell) -> float:
        dx, dy = abs(source.x - goal.x), abs(source.y - goal.y)
        return np.sqrt(2) if dx + dy == 2 else 1.0

    def compute_path(self, source: GridCell, goal: GridCell) -> Path:
        if not self.env.in_bounds(source) or self.env.is_occupied(source):
            raise Exception("Source is not a valid position")
        if not self.env.in_bounds(goal) or self.env.is_occupied(goal):
            raise Exception("Goal is not a valid position")

        tie_count = 0
        open_set = []
        heapq.heappush(open_set, (0.0, tie_count, source))

        came_from = {source: None}
        cost_so_far = {source: 0.0}
        closed_set = set()  # track fully explored cells

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current in closed_set:  # already explored optimally, skip
                continue

            closed_set.add(current)

            if current == goal:
                break

            for next_cell in self.env.get_neighbors(current):
                if self.env.is_occupied(next_cell) or next_cell in closed_set:
                    continue
                new_cost = cost_so_far[current] + self.cost(current, next_cell)
                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + self.heuristic(next_cell, goal)
                    tie_count += 1
                    heapq.heappush(open_set, (priority, tie_count, next_cell))
                    came_from[next_cell] = current

        if current != goal:
            raise Exception("Path not found")

        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path
