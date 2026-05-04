from seally.common.path import Path
from seally.env.grid_map import GridCell, GridMap
from collections import deque
import copy

class WaveFront():
    """
    Wave Front Algorithm for finding the shortest path between points in a GridMap.
    """
    def __init__(self, env: GridMap):
        """
        Initialize a WaveFront Object.

        Args:
            env: A grid base environment.
        """
        self.env = env
        self.wave_field = copy.deepcopy(env)
        self._closed_set = set()  # track fully explored cells
        self._goal_dist = 2 # Defualt Goal distance value

    def calc_wavefront(self, goal: GridCell) -> None:
        """
        Generates a wave front by calculating the distance from each cell in the GridMap to the goal.

        Args:
            goal: The goal cell in the GridMap.
        """
        queue = deque([goal])
        self._closed_set.add(goal)

        while queue:
            # Get the oldest cell in the queue
            current = queue.popleft()

             # Get all the neighbors of the cell
            for n in self.env.get_neighbors(current):
                # The Wave value for each neighbor cell is the current value plus 1
                if not self.env.is_occupied(n) and n not in self._closed_set:
                    self.wave_field.map[n.y, n.x] = self.wave_field.map[current.y, current.x] + self.env.get_cost(current, n)

                    self._closed_set.add(n) # Add the visited cell to the closed set
                    queue.append(n) # add the cell back into the queue so that it can be visited

    def compute_path(self, source: GridCell, goal: GridCell) -> Path:
        """
        Computes the shortest path from the source GridCell to the goal GridCell using the Wave Front Algorithm.

        Args:
            source: The source cell in the GridMap.
            goal: The goal cell in the GridMap.

        Returns:
            A path from source to goal.
        """

        # reset class variavbles
        self.wave_field = copy.deepcopy(self.env)
        self._closed_set = set()

        if not self.env.in_bounds(source) or self.env.is_occupied(source):
            raise Exception("Source is not a valid position")
        
        if not self.env.in_bounds(goal) or self.env.is_occupied(goal):
            raise Exception("Goal is not a valid position")
                
        # Set the goals distance value in the wave_feild
        self.wave_field.map[goal.y, goal.x] = self._goal_dist

        # Add the goal to the closed set
        self._closed_set.add(goal)

        # Expand a wave from the goal to the source position
        self.calc_wavefront(goal)

        path = []
        current = source

        # Traverse the Wave Feild from the source to the goal
        while current != goal:
            path.append(current)
            neighbors = self.env.get_neighbors(current)
            
            next_cell = None
            next_val = float('inf')
            
            # Find the neighbor with the lowest wave value
            for n in neighbors:
                if self.env.is_occupied(n):
                    continue

                val = self.wave_field.map[n.y, n.x]
                if val > 0 and val < next_val:
                    next_cell = n
                    next_val = val
            
            # Path could not be found
            if next_cell is None or next_cell == current:
                raise Exception("Goal is unreachable from current position")
            
            # Visit Next cell
            current = next_cell

        path.append(goal)
        return path

        