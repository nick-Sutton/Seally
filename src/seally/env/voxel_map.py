from typing import List
import numpy as np
import pandas as pd
from seally.env.enviroment import Position, Enviroment, Dimensions

# https://bink.eu.org/fast-voxel-datastructures/

class VoxelCell(Position):
    """
    Cell in a VoxelMap
    """
    def __init__(self, dims: Dimensions):
        """
        TODO: Write Comment
        """
        super().__init__(dims) 
        self.i = Dimensions[0]
        self.j = Dimensions[1]
        self.k = Dimensions[2]

    def __hash__(self):
        return hash((self.i, self.j, self.k))

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j and self.k == other.k

class VoxelMap:
    """
    TODO: Comment
    """
    def __init__(self, gen_random: bool = True, file_path: str = None):
        """
        TODO: Comment
        """
        if gen_random:
            pass
        else:
            self.map = pd.read_csv(file_path).to_numpy()

        self.i_dim = self.map.shape[1]
        self.j_dim = self.map.shape[0]
        self.k_dim = self.map.shape[2]

    def is_occupied(self, voxel: VoxelCell) -> bool:
        """
        TODO: Comment
        """
        return self.map[voxel.j, voxel.i, voxel.k] > 0
    
    def in_bounds(self, voxel: VoxelCell) -> bool:
        """
        TODO: Comment
        """

        if voxel.i < 0 or voxel.i > self.i_dim - 1:
            return False
        
        if voxel.j < 0 or voxel.j > self.j_dim - 1:
            return False
        
        if voxel.k < 0 or voxel.k > self.k_dim - 1:
            return False
        
        return True

    def get_neighbors(self, cell: GridCell) -> List[GridCell]:
        """
        Retuns a list of all valid neighbors for a given cell in the Gripmap
        A valid cell is a cell that is within the bounds of the map.

        Args:
            cell: The cell whose neighbors to retrieve.

        Returns:
            A list of the cells valid neighbors.
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