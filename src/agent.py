import numpy as np
from enum import Enum
from src.world import *


class Dir(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    STAY = 4

class Agent:

    def __init__(self, begin: tuple[int,int], objective: tuple[int,int], world: World, id: int) -> None:
        self.id = id
        self.position = begin
        self.objective = objective
        self.world = world


    def move(self, grid: np.ndarray, direction: Dir) -> bool:
        can_move = False
        if direction == Dir.UP:
            new_position = (self.position[0] - 1, self.position[1])
            can_move = self.check_move_possible(grid, new_position)
        elif direction == Dir.LEFT:
            new_position = (self.position[0], self.position[1] - 1)
            can_move = self.check_move_possible(grid, new_position)
        elif direction == Dir.DOWN:
            new_position = (self.position[0] + 1, self.position[1])
            can_move = self.check_move_possible(grid, new_position)
        elif direction == Dir.RIGHT:
            new_position = (self.position[0], self.position[1] + 1)
            can_move = self.check_move_possible(grid, new_position)
        else:
            new_position = (self.position[0], self.position[1])
            can_move = True
        if not can_move:
            return False
        else:
            self.world.grid[new_position] = self.id
            self.world.grid[self.position] = -1
            self.position = new_position
            return True
        
    
    def check_move_possible(self, grid: np.ndarray, coordinates: tuple[int,int]) -> bool:
        if coordinates[0] < 0 or coordinates[0] >= grid.shape[0] or coordinates[1] < 0 or coordinates[1] >= grid.shape[1]:
            return False
        if grid[coordinates] == -1:
            return False
        return True

