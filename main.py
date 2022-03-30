from src.world import *
#from src.agent import *


def main():

    a = World(10, 0.2,3)
    a.show()

    print(a.check_validity(5, 0.7))
    a.agents[0].move(a.grid, Dir.UP)
    a.show()
    print(np.sum(a.grid == -1))

if __name__=="__main__":
   main()