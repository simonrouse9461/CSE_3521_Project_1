from puzzle import *
from search_agent import SearchAgent


def generate_test_problem(problem):
    if problem == 'shuffle':
        state = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
        state.shuffle(100)
        return state
    elif problem == 'easy':
        state = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
        state.shuffle(15)
        return state
    elif problem == 'random':
        return Puzzle.random_puzzle()
    elif problem == 'project':
        return Puzzle(5, 0, 4, 2, 1, 3, 6, 7, 8)
    elif problem == 'unsolvable':
        return Puzzle(0, 2, 1, 3, 4, 5, 6, 7, 8)
    else:
        return Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)

init = generate_test_problem('shuffle')
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
