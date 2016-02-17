from puzzle import *


p = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
q = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)

#prob = Problem(p, q)
#r = prob.result(p, Puzzle.down)
#print(r)


q.move(Puzzle.down, Puzzle.right)
print(p)
print(q)

prob = Problem(p, q)
search = TreeSearch(prob)
result = search.depth_limited_search(2)
print(result)
