import numpy as np
from matplotlib import pyplot as plt

class World:
    def __init__(self, size, obstacle_proportion) -> None:
        self.size = size
        self.grid = np.zeros((size,size))
        self.obstacle_proportion = obstacle_proportion
        self.add_obstacles()

    def add_obstacles(self):
        n_obstacles = int(self.size**2 * self.obstacle_proportion)
        k = 0
        
        while k < n_obstacles:
            i = np.random.randint(0,self.size)
            j = np.random.randint(0,self.size)
            k += self.add_one_obstacle(i,j)


    def add_one_obstacle(self, i,j):
        if i < 0 or i >= self.size or j < 0 or j >= self.size:
            print("Incorrect coordinates")
            return False
        if self.grid[i,j] == -1:
            return False
        self.grid[i,j] = -1
        return True

    def show(self):
        plt.figure()
        plt.imshow(self.grid, cmap='gray')
        plt.show()