from puzzle import *
from search_agent import SearchAgent


goal = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
init = goal.copy
init.shuffle(15)

print('Initial state:', init)
print('Goal state:', goal)
print('Heuristic:', init.dist(goal))
print()

prob = PuzzleProblem(initial_state=init, goal_state=goal)
agent = SearchAgent(prob)
result = agent.a_star_search()
print()

print('Result:', result)
