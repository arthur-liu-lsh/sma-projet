from src.world import *
#from src.agent import *


def main():

    a = World(10, 0.01,3, "EpsGreedy", True, 0.1)
    # a.show()
    a.init_plot()
    print(a.check_validity(5, 0.7))
    nb_iter = a.simulate()
    
    print(nb_iter)

if __name__=="__main__":
   main()