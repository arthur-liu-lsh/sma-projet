from src.world import *

a = World(10, 0.2,3)
a.show()

b = Agent((0,0), (1,1))
print(b.position)
b.move(a.grid, Dir.UP)
print(b.position)
b.move(a.grid, Dir.DOWN)
print(b.position)
b.move(a.grid, Dir.RIGHT)
print(b.position)
print(a.check_validity())
print(a.grid)
print(np.sum(a.grid == -1))