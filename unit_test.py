from puzzle import *


goal = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
init = goal.copy
init.shuffle(15)

print('Initial state:', init)
print('Goal state:', goal)
print('Heuristic:', init.heuristic(goal))
print()

prob = Problem(initial_state=init, goal_state=goal)
search = TreeSearch(prob)
result = search.iterative_deepening_search()
print()

print('Result:', result)
