from src.world import *
#from src.agent import *


def main():

    # a.show()
    
    n_iter = 100

    sum = 0
    for i in range(n_iter):
        world_EpsGreedy = World(10, 0.2,3, "EpsGreedy", False, 0.1)
        while not world_EpsGreedy.check_validity(5, 0.7):
            world_EpsGreedy = World(10, 0.2,3, "EpsGreedy", False, 0.1)
        sum += world_EpsGreedy.simulate()
    
    print("EpsGreedy 10x10, 20", "%", "d'obstacles", n_iter, "itérations :",sum/n_iter)

    sum = 0
    for i in range(n_iter):
        world_AStar = World(10, 0.2,3, "A*", False, 0.1)
        while not world_AStar.check_validity(5, 0.7):
            world_AStar = World(10, 0.2,3, "AStar", False, 0.1)
        sum += world_AStar.simulate()
    
    print("A*",sum/n_iter)

if __name__=="__main__":
   main()