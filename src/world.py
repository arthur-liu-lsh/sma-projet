import string
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


    def chose_move(self, grid: np.ndarray, direction: Dir) -> bool:
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
            self.world.grid[self.position] = -1
            self.world.grid[new_position] = self.id
            self.position = new_position
            return True


    def check_move_possible(self, grid: np.ndarray, coordinates: tuple[int,int]) -> bool:
        if coordinates[0] < 0 or coordinates[0] >= grid.shape[0] or coordinates[1] < 0 or coordinates[1] >= grid.shape[1]:
            return False
        if grid[coordinates] != -1:
            return False
        return True

    def chose_action(self, grid: np.ndarray):
        self.chose_move(grid, np.random.choice(list(Dir)))
        # Réimplémenter la fonction dans les classes qui héritent de Agent

class EpsGreedy(Agent):
    def chose_action(self, grid: np.ndarray):
        eps = 0.25
        p = np.random.rand()
        if self.objective != self.position:
            if p < eps:
                self.chose_move(grid, np.random.choice(list(Dir)))
            else:
                if self.position[0] > self.objective[0]:
                    if grid[self.position[0]-1, self.position[1]] == -1:
                        self.chose_move(grid, Dir.UP)
                        return None
                if self.position[0] < self.objective[0]:
                    if grid[self.position[0]+1, self.position[1]] == -1:
                        self.chose_move(grid, Dir.DOWN)
                        return None
                if self.position[1] > self.objective[1]:
                    if grid[self.position[0], self.position[1]-1] == -1:
                        self.chose_move(grid, Dir.LEFT)
                        return None
                if self.position[1] < self.objective[1]:
                    if grid[self.position[0], self.position[1]+1] == -1:
                        self.chose_move(grid, Dir.RIGHT)
                        return None
                self.chose_move(grid, np.random.choice(list(Dir)))
                return None
        else:
            self.chose_move(grid, Dir.STAY)
        return None

class AStarAgent(Agent):
    def chose_action(self, grid: np.ndarray):
        new_position = self.find_next_position(grid)
        self.world.grid[self.position] = -1
        self.world.grid[new_position] = self.id
        self.position = new_position

    def find_next_position(self, grid):
        queue = []
        gn = 0
        objective = self.objective
        fn = h(grid, self.position, objective)
        if fn == -1 :
            return self.position #si pas de possibilité d'accéder à l'objectif, on attend à la même case   
        queue.append([gn, fn, self.position])
        checked = []
        while queue:
            test1 = [x[1] for x in queue]
            ind = test1.index(min(test1))
            node = queue.pop(ind)
            coord = node[2]
            if coord == self.objective:
                return reconstruct_path(checked, self.position, self.objective)
            else:
                gn = node[0]+1
                test2 = [x[1] for x in checked]
                
                if coord[0] -1 >= 0 and grid[coord[0]-1][coord[1]]==-1:
                    new_coord = (coord[0]-1, coord[1])
                    test3 = [x[0] for x in queue if x[2]==new_coord]
                    if not new_coord in test2 and all(i >= gn for i in test3):
                        res = h(grid, new_coord, objective)
                        if res > -1:
                            fn = gn + res
                            checked.append([coord, new_coord, fn])
                            queue.append([gn, fn, new_coord])


                if coord[0] + 1 <grid.shape[0] and grid[coord[0]+1][coord[1]]==-1:
                    new_coord = (coord[0]+1, coord[1])
                    test3 = [x[0] for x in queue if x[2]==new_coord]
                    if not new_coord in test2 and all(i >= gn for i in test3):
                        res = h(grid, new_coord, objective)
                        if res > -1:
                            fn = gn + res
                            checked.append([coord, new_coord, fn])
                            queue.append([gn, fn, new_coord])


                if coord[1] -1 >= 0 and grid[coord[0]][coord[1]-1]==-1:
                    new_coord = (coord[0], coord[1]-1)
                    test3 = [x[0] for x in queue if x[2]==new_coord]
                    if not new_coord in test2 and all(i >= gn for i in test3):
                        res = h(grid, new_coord, objective)
                        if res > -1:
                            fn = gn + res
                            checked.append([coord, new_coord, fn])
                            queue.append([gn, fn, new_coord])


                if coord[1] + 1 <grid.shape[1] and grid[coord[0]][coord[1]+1]==-1:
                    new_coord = (coord[0], coord[1]+1)
                    test3 = [x[0] for x in queue if x[2]==new_coord]
                    if not new_coord in test2 and all(i >= gn for i in test3):
                        res = h(grid, new_coord, objective)
                        if res > -1:
                            fn = gn + res
                            checked.append([coord, new_coord, fn])
                            queue.append([gn, fn, new_coord])
        return self.position



class World:
    def __init__(self, size: int, p_obstacles: float, n_agents: int, agent_type:string, plot_world = True, plot_delay: float = 0.5) -> None:
        self.size = size
        self.grid = - np.ones((size,size))
        self.p_obstacles = p_obstacles
        self.n_agents = n_agents
        self.agent_type = agent_type
        self.generate_obstacles()
        self.agents = self.generate_agents()
        self.plot_world = plot_world
        self.plot_delay = plot_delay

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
                assert k<100, 'Fail to initialize agents'    
                i1, j1 = np.random.randint(self.size), np.random.randint(self.size)
                i2, j2 = np.random.randint(self.size), np.random.randint(self.size)
                if self.grid[i1][j1] == -1 and self.grid[i2][j2] == -1:
                    agent = self.generate_one_agent((i1,j1), (i2,j2), i)
                    agents.append(agent)
                    break
                k+=1
        return agents

    def generate_one_agent(self, begin, objective, id) -> Agent:
        if self.agent_type == "A*":
            return AStarAgent(begin, objective, self, id)
        elif self.agent_type == "EpsGreedy":
            return EpsGreedy(begin, objective, self, id)
        else:
            return Agent(begin, objective, self, id)

    def init_plot(self) -> None:
        if self.plot_world:
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
        if self.plot_delay > 0:
            plt.pause(self.plot_delay)
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

    def objective_attained(self) -> bool:
        for a in self.agents:
            if a.position != a.objective:
                return False
        return True

    def one_iter(self) -> None:
        for a in self.agents:
            if a.position != a.objective:
                a.chose_action(self.grid)

    def simulate(self) -> int:
        go = not self.objective_attained()
        count = 0
        while go and count < 1000:
            self.one_iter()
            if self.plot_world:
                self.show()
            go = not self.objective_attained()
            count += 1
        return count


def h(grid, init, obj):
    cgrid = np.copy(grid)
    cgrid[cgrid>=0] = -2
    i =0
    cgrid[init[0]][init[1]]=0
    cond = True
    while cond:
        coords = np.argwhere(cgrid == i)
        modif = False
        for coord in coords:
            if coord[0] -1 >= 0 and cgrid[coord[0]-1][coord[1]]==-1:
                cgrid[coord[0]-1][coord[1]]=i+1
                modif = True
            if coord[0] + 1 <cgrid.shape[0] and cgrid[coord[0]+1][coord[1]]==-1:
                cgrid[coord[0]+1][coord[1]]=i+1
                modif = True
            if coord[1] -1 >= 0 and cgrid[coord[0]][coord[1]-1]==-1:
                cgrid[coord[0]][coord[1]-1]=i+1
                modif = True
            if coord[1] + 1 <cgrid.shape[1] and cgrid[coord[0]][coord[1]+1]==-1:
                cgrid[coord[0]][coord[1]+1]=i+1
                modif = True
        i+=1
        if cgrid[obj[0]][obj[1]]!=-1 or not modif:
            cond = False
    return cgrid[obj[0]][obj[1]]

def reconstruct_path(checked, init, obj):
    current = obj
    while True:
        test = [x[1] for x in checked]
        ind = test.index(current)
        res = checked[ind][0]
        if res == init:
            return current
        current = res



def a_star(grid, agent):
    queue = []
    gn = 0
    objective = agent.objective
    fn = h(grid, agent.position, objective)
    if fn == -1 :
        return agent.position #si pas de possibilité d'accéder à l'objectif, on attend à la même case   
    queue.append([gn, fn, agent.position])
    checked = []
    while queue:
        test1 = [x[1] for x in queue]
        ind = test1.index(min(test1))
        node = queue.pop(ind)
        coord = node[1]
        if coord == node[2]:
            return reconstruct_path(checked)
        else:
            gn = node[0]+1
            test2 = [x[1] for x in checked]
            
            if coord[0] -1 >= 0 and grid[coord[0]-1][coord[1]]==-1:
                new_coord = (coord[0]-1, coord[1])
                test3 = [x[0] for x in queue if x[2]==new_coord]
                if not new_coord in test2 and all(i >= gn for i in test3):
                    res = h(grid, new_coord, objective)
                    if res > -1:
                        fn = gn + res
                        checked.append([coord, new_coord, fn])
                        queue.append([gn, fn, new_coord])


            if coord[0] + 1 <grid.shape[0] and grid[coord[0]+1][coord[1]]==-1:
                new_coord = (coord[0]+1, coord[1])
                test3 = [x[0] for x in queue if x[2]==new_coord]
                if not new_coord in test2 and all(i >= gn for i in test3):
                    res = h(grid, new_coord, objective)
                    if res > -1:
                        fn = gn + res
                        checked.append([coord, new_coord, fn])
                        queue.append([gn, fn, new_coord])


            if coord[1] -1 >= 0 and grid[coord[0]][coord[1]-1]==-1:
                new_coord = (coord[0], coord[1]-1)
                test3 = [x[0] for x in queue if x[2]==new_coord]
                if not new_coord in test2 and all(i >= gn for i in test3):
                    res = h(grid, new_coord, objective)
                    if res > -1:
                        fn = gn + res
                        checked.append([coord, new_coord, fn])
                        queue.append([gn, fn, new_coord])


            if coord[1] + 1 <grid.shape[1] and grid[coord[0]][coord[1]+1]==-1:
                new_coord = (coord[0], coord[1]+1)
                test3 = [x[0] for x in queue if x[2]==new_coord]
                if not new_coord in test2 and all(i >= gn for i in test3):
                    res = h(grid, new_coord, objective)
                    if res > -1:
                        fn = gn + res
                        checked.append([coord, new_coord, fn])
                        queue.append([gn, fn, new_coord])
    return None