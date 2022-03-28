import numpy as np
from matplotlib import pyplot as plt
from src.agent import *

class World:
    def __init__(self, size: int, p_obstacles: float, n_agents: int) -> None:
        self.size = size
        self.grid = np.zeros((size,size))
        self.p_obstacles = p_obstacles
        self.generate_obstacles()
        self.generate_agents()

    def generate_obstacles(self) -> None:
        n_obstacles = int(self.size**2 * self.p_obstacles)
        k = 0
        
        while k < n_obstacles:
            i = np.random.randint(0,self.size)
            j = np.random.randint(0,self.size)
            k += self.generate_one_obstacle(i,j)


    def generate_one_obstacle(self, i: int, j: int) -> bool:
        if i < 0 or i >= self.size or j < 0 or j >= self.size:
            print("Incorrect coordinates")
            return False
        if self.grid[i,j] == -1:
            return False
        self.grid[i,j] = -1
        return True

    def generate_agents(self) -> None:
        pass

    def generate_one_agent(self, begin, objective) -> Agent:
        return Agent(begin, objective)

    def show(self) -> None:
        plt.figure()
        plt.imshow(self.grid, cmap='gray')
        plt.show()