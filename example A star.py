from src.world import *


def main():

    world_AStar = World(10, 0.2,5, "A*", True, 0.25)
    while not world_AStar.check_validity(5, 0.7):
        world_AStar = World(10, 0.2,5, "AStar", True, 0.25)
    world_AStar.print_objectives()
    n_iter = world_AStar.simulate()
    
    print("A*",n_iter, "iterations")

if __name__=="__main__":
   main()