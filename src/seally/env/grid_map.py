from typing import List, Optional
import numpy as np
import pandas as pd

from seally.env.environment import Dimensions, Environment, Position

class GridCell(Position):
    """
    Cell in a GridMap
    """
    def __init__(self, dims: Dimensions):
        """
        Initialize a GridCell Object.

        Args:
            dims: A Tuple of Integers representing an index into the Grid Map.
        """
        super().__init__(dims) 
        self.x = dims[0]
        self.y = dims[1]

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class GridMap(Environment):
    """
    Grid based discritization of an enviroment. GridMaps store enviroments as a numpy array 
    where the value at each cell is either 0 if the cell is free and 1 if it is occupied.
    """
    def __init__(self, gen_random: bool = True, file_path: Optional[str] = None, move_4d: bool = False):
        """
        Initialize a GridMap Object.

        Args:
            gen_random: Boolean for if the Map should be generated randomly.
            file_path: Path to map file.
            move_4d: Boolean for if the neighborhood of a given cell includes the cells on its diagonals
        """
        if gen_random:
            pass
        else:
            if file_path is None:
                raise ValueError("file_path must be provided when gen_random is False")
            self.map = pd.read_csv(file_path).to_numpy()

        self.x_dim = self.map.shape[1]
        self.y_dim = self.map.shape[0]

        self._move_4d = move_4d


    def get_cost(self, source: Position, goal: Position) -> float:
        """
        Computes the cost of going from the source cell the goal cell. 
        For GridMaps the cost is sqrt(2) for diagonal cells and 1 otherwise.

        Args:
            source: The source cell in the GridMap.
            goal: The goal cell in the GridMap.

        Returns:
            The cost of going from source to goal.
        """
        if self._move_4d:
            return 0.0
        else:
            dx, dy = abs(source.dim_array[0] - goal.dim_array[0]), abs(source.dim_array[1] - goal.dim_array[1])
            return np.sqrt(2) if dx + dy == 2 else 1.0

    def is_occupied(self, cell: Position) -> bool:
        """
        Determines if the provided coordinates are in collision with an obstacle.

        Args:
            cell: Cell to check.

        Returns: 
            True if the position is in collision.
        """
        return self.map[cell.dim_array[1], cell.dim_array[0]] > 0
    
    def in_bounds(self, cell: Position) -> bool:
        """
        Determines if the provided coordinates within the bounds of the map.

        Args: 
            cell: Cell to check.

        Returns: 
            True if the position is in bounds.
        """

        if cell.dim_array[0] < 0 or cell.dim_array[0] > self.x_dim - 1:
            return False
        
        if cell.dim_array[1] < 0 or cell.dim_array[1] > self.y_dim - 1:
            return False
        
        return True

    def get_neighbors(self, cell: Position) -> List[Position]:
        """
        Retuns a list of all valid neighbors for a given cell in the Gripmap
        A valid cell is a cell that is within the bounds of the map.

        Args:
            cell: The cell whose neighbors to retrieve.

        Returns:
            A list of the cells valid neighbors.
        """

        # create a mask of the indicies of the neighboring cells relative to the current cell 
        shift_mask = None
        if self._move_4d:
            shift_mask = np.array([     [-1,0],
                                [0,-1],         [0,1],
                                        [1,0]])
        else:
            shift_mask = np.array([[-1,-1],[-1,0],[-1,1],
                                   [0,-1],         [0,1],
                                   [1,-1], [1,0], [1,1]])
        
        # broadcast the current cell to each of the shift mask offsets and add them to produce an array of neighbor coordinates
        neighbor_indicies = np.array([cell.dim_array[1], cell.dim_array[0]]) + shift_mask

        # create a mask to validate that all cells are in the bounds of the map
        bounds_mask = (
            (neighbor_indicies[:, 0] >= 0) & (neighbor_indicies[:, 0] < self.y_dim) &
            (neighbor_indicies[:, 1] >= 0) & (neighbor_indicies[:, 1] < self.x_dim)
        )

        # apply the bounds map to each coordinate and return only the cells that are in bounds
        return [GridCell((col, row)) for row, col in neighbor_indicies[bounds_mask]]