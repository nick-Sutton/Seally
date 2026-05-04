from typing import List, Tuple, Union
import numpy as np
from abc import ABC, abstractmethod

Dimensions = Union[Tuple[int, ...], Tuple[float, ...]]

class Position(ABC):
    """
    Cell in a GridMap
    """
    def __init__(self, dims: Dimensions):
        """
        !TODO: Add comment

        dim_array = numpy array
        """
        self.dim_array = np.asarray(dims)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Environment(ABC):
    @abstractmethod
    def get_cost(self, start: Position, end: Position) -> float:
        pass

    @abstractmethod
    def is_occupied(self, pos: Position) -> bool:
        """
        !TODO: ADD comment
        """
        pass
    
    @abstractmethod
    def in_bounds(self, pos: Position) -> bool:
        """
        !TODO Add Comment
        """
        pass

    @abstractmethod
    def get_neighbors(self, position: Position) -> List[Position]:
        """
        !TODO: Add Comment
        """ 
        pass

    """
    @abstractmethod
    def sample_position(self):
        TODO: Add Comment
        pass
    """