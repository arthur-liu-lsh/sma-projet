import numpy as np
from matplotlib import pyplot as plt
from enum import Enum
from matplotlib import colors


class Dir(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    STAY = 4

class Agent:

    def __init__(self, begin: tuple[int,int], objective: tuple[int,int], world, id: int) -> None:
        self.id = id
        self.position = begin
        self.objective = objective
        self.world = world
        self.world.grid[begin] = id


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
        if grid[coordinates] != -1:
            return False
        return True





class World:
    def __init__(self, size: int, p_obstacles: float, n_agents: int) -> None:
        self.size = size
        self.grid = - np.ones((size,size))
        self.p_obstacles = p_obstacles
        self.n_agents = n_agents
        self.generate_obstacles()
        self.agents = self.generate_agents()

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

    def generate_agents(self) -> list:
        agents = []
        for i in range(self.n_agents):
            k = 0
            while True:
                print(k)
                assert k<100, 'Fail to initialize agents'    
                i1, j1 = np.random.randint(self.size), np.random.randint(self.size)
                i2, j2 = np.random.randint(self.size), np.random.randint(self.size)
                if self.grid[i1][j1] == -1 and self.grid[i2][j2]:
                    agent = self.generate_one_agent((i1,j1), (i2,j2), i)
                    agents.append(agent)
                    break
                k+=1
        return agents

    def generate_one_agent(self, begin, objective, id) -> Agent:
        return Agent(begin, objective, self, id)

    def init_plot(self) -> None:
        plt.figure()
        self.show()

    def show(self) -> None:

        cmap = colors.ListedColormap(['black', 'white', 'blue'])
        bounds = [-2,-1,0, self.n_agents]
        norm = colors.BoundaryNorm(bounds, cmap.N)
 
        
        #fig, ax = plt.subplots()
        plt.clf()
        plt.imshow(self.grid, cmap=cmap, norm=norm)
        for i in range(self.size):
            for j in range(self.size):
                x = self.grid[i][j]
                if x>= 0:
                    c = str(int(x))
                else:
                    c = ''
                plt.text(j, i, c, va='center', ha='center')


        # draw gridlines
        plt.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        plt.xticks(np.arange(-0.5, self.size, 1))
        plt.yticks(np.arange(-0.5, self.size, 1))
        plt.pause(0.5)
        # plt.show()


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