from puzzle import *
from search_agent import SearchAgent


init = Puzzle(5, 0, 4, 2, 1, 3, 6, 7, 8)
prob = PuzzleProblem(initial_state=init)

print()
print('Initial state:\n', init)
print('Goal state:\n', prob.goal_state)
print('Heuristic:', init.dist(prob.goal_state))
print()

agent = SearchAgent(prob)
agent.a_star_search()
print()
agent.print_solution()
