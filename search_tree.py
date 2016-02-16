from puzzle import Puzzle


class SearchTree:

    class NoResult:
        failure = -1
        cutoff = 0

        def __init__(self, value):
            self.value = value

    class Result:

        def __init__(self, solution):
            self.solution = solution

    class Node:
        pass

    def __init__(self, initial, goal):
        if type(initial) is not Puzzle or type(goal) is not Puzzle:
            raise Exception('initial state and goal state must be Puzzle')
        self.initial = initial
        self.goal = goal
        self.__frontier_stack = [initial]

    def add_frontier(self, frontier):
        self.__frontier_stack.insert(0, frontier)

    def remove_frontier(self):
        return self.__frontier_stack.pop(0)

    @staticmethod
    def __make_node(state, parent, action, depth):
        node = SearchTree.Node()
        node.state = state
        node.parent = parent
        node.action = action
        node.depth = depth
        return node

    def expand_node(self):
        frontier = self.remove_frontier()
        if frontier.state == self.goal:
            return True
        for action in Puzzle.actions:
            if frontier.state.can_move(action):
                child_state = frontier.copy
                child_state.move(action)
                child_node = self.__make_node(child_state, frontier, action, frontier.depth + 1)
                self.add_frontier(child_node)
        return False

