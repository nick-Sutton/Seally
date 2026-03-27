from typing import List

import numpy as np
import pandas as pd

class GridCell():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class GridMap:
    def __init__(self, gen_random: bool = True, file_path: str = None):
        if gen_random:
            pass
        else:
            self.map = pd.read_csv(file_path).to_numpy()

        self.x_dim = self.map.shape[1]
        self.y_dim = self.map.shape[0]

    def is_occupied(self, cell: GridCell) -> bool:
        """
        Determines if the provided coordinates are in collision with an obstacle

        param: cell to check
        return: True if the position is in collision
        """
        return self.map[cell.y, cell.x] > 0
    
    def in_bounds(self, cell: GridCell) -> bool:
        """
        Determines if the provided coordinates within the bounds of the map

        param: cell to check
        return: True if the position is in bounds
        """

        if cell.x < 0 or cell.x > self.x_dim - 1:
            return False
        
        if cell.y < 0 or cell.y > self.y_dim - 1:
            return False
        
        return True

    def get_neighbors(self, cell: GridCell) -> List[GridCell]:
        """
        Retuns a list of all valid neighbors for a given cell in the Gripmap
        A valid cell is a cell that is within the bounds of the map.

        params: cell to retrieve neighbors for
        returns: A list of the cells valid neighbors
        """

        # create a mask of the indicies of the neighboring cells relative to the current cell        
        shift_mask = np.array([[-1,-1],[-1,0],[-1,1],
                               [0,-1],         [0,1],
                               [1,-1], [1,0], [1,1]])
        
        # broadcast the current cell to each of the shift mask offsets and add them to produce an array of neighbor coordinates
        neighbor_indicies = np.array([cell.x, cell.y]) + shift_mask  # shape (8, 2)

        # create a mask to validate that all cells are in the bounds of the map
        bounds_mask = (
            (neighbor_indicies[:, 0] >= 0) & (neighbor_indicies[:, 0] < self.x_dim) &
            (neighbor_indicies[:, 1] >= 0) & (neighbor_indicies[:, 1] < self.y_dim)
        )

        # apply the bounds map to each coordinate and return only the cells that are in bounds
        return [GridCell(x, y) for x, y in neighbor_indicies[bounds_mask]]