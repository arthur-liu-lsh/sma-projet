import numpy as np
from matplotlib import pyplot as plt
from src.agent import *
from matplotlib import colors


class World:
    def __init__(self, size: int, p_obstacles: float, n_agents: int) -> None:
        self.size = size
        self.grid = - np.ones((size,size))
        self.p_obstacles = p_obstacles
        self.n_agents = n_agents
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
        if self.grid[i,j] == -2:
            return False
        self.grid[i,j] = -2
        return True

    def generate_agents(self) -> None:
        pass

    def generate_one_agent(self, begin, objective) -> Agent:
        return Agent(begin, objective)

    def show(self) -> None:
        plt.figure()

        cmap = colors.ListedColormap(['black', 'white', 'blue'])
        bounds = [-2,-1,0, self.n_agents]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        while True:
            i,j = np.random.randint(self.size), np.random.randint(self.size)
            if self.grid[i][j] == -1:
                self.grid[i][j] =0
                break
        
        #fig, ax = plt.subplots()
        plt.imshow(self.grid, cmap=cmap, norm=norm)
        for i in range(self.size):
            for j in range(self.size):
                x = self.grid[i][j]
                if x>= 0:
                    c = str(x)
                else:
                    c = ''
                plt.text(j, i, c, va='center', ha='center')


        # draw gridlines
        plt.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        plt.xticks(np.arange(-0.5, self.size, 1))
        plt.yticks(np.arange(-0.5, self.size, 1))
        plt.show()


    def check_validity_rec(self, arr, row, col, first) -> None:
        if first :
            row, col = (np.random.randint(self.size), np.random.randint(self.size))
        arr[row][col] = -3
        voisins = [(row+1,col),(row-1,col),(row,col-1),(row,col+1)]
        for voisin in voisins:
            (v_row,v_col) = voisin
            if v_row>=0 and v_row<self.size and v_col>=0 and v_col<self.size:
                if arr[v_row][v_col]==-1:
                    self.check_validity_rec(arr,v_row,v_col, False)

    def check_validity_kernel(self, valid_ratio) -> bool:
        test = np.copy(self.grid)
        self.check_validity_rec(test, 0, 0, True)
        percentage = np.sum(test == -3)/((self.size)**2-np.sum(test == -2))
        if percentage >= valid_ratio :
            return True
        else:
            return False

    def check_validity(self, nb_check, valid_ratio) -> bool:
        for i in range(nb_check):
            res = self.check_validity_kernel(valid_ratio)
            if res == True:
                break
        return res