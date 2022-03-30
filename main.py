from src.world import *
#from src.agent import *


def main():

    a = World(10, 0.2,3, "A*", True, 0.5)
    # a.show()
    a.init_plot()
    print(a.check_validity(5, 0.7))
    nb_iter = a.simulate()
    
    print(np.sum(a.grid == -1))

if __name__=="__main__":
   main()