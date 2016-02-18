from puzzle import *
from search_agent import SearchAgent


def generate_test_problem(goal, problem):
    if problem == 'shuffle':
        state = goal.copy
        state.shuffle(100)
        return state
    elif problem == 'random':
        return Puzzle.random_puzzle()
    elif problem == 'project':
        return Puzzle(5, 0, 4, 2, 1, 3, 6, 7, 8)
    elif problem == 'unsolvable':
        return Puzzle(0, 2, 1, 3, 4, 5, 6, 7, 8)
    else:
        return goal

goal = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
init = generate_test_problem(goal, 'shuffle')

print('Initial state:', init)
print('Goal state:', goal)
print('Heuristic:', init.dist(goal))
print()

prob = PuzzleProblem(initial_state=init, goal_state=goal)
agent = SearchAgent(prob)
result = agent.a_star_search()
print()

print('Result:', result)
