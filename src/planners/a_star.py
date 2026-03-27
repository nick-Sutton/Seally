from typing import Tuple
from planners.path import Path
import heapq
import numpy as np

from env.enviroment import Enviroment
import networkx as nx

class AStar:
    # https://www.redblobgames.com/pathfinding/a-star/introduction.html
    def __init__(self):
        pass

    def plan(self, source: Tuple[float, float] , goal: Tuple[float, float] , env: Enviroment) -> Path:

        open_set = []
        heapq.heappush(open_set, (source, 0))

        came_from = {}
        cost_so_far = {}

        came_from[source] = np.inf
        cost_so_far[source] = 0

        while not open_set:
            current = heapq.heappop()

            if current == goal:
                break

            for next in 

        '''
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
        '''

