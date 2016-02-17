import random


class Puzzle:

    class Action:

        def __init__(self, row, col):
            self.row = row
            self.col = col

        def __repr__(self):
            if self.value == (-1, 0):
                return 'Up'
            if self.value == (1, 0):
                return 'Down'
            if self.value == (0, -1):
                return 'Left'
            if self.value == (0, 1):
                return 'Right'

        @property
        def value(self):
            return self.row, self.col

        @property
        def raw(self):
            return self.row * 3 + self.col

    up = Action(-1, 0)
    down = Action(1, 0)
    left = Action(0, -1)
    right = Action(0, 1)
    action_set = {up, down, left, right}

    def __init__(self, *args):
        if len(args) != 9:
            raise Exception('9 arguments expected')
        if len(set(args)) != 9:
            raise Exception('arguments must be unique')
        self.__list = [0] * 9
        for i, num in enumerate(args):
            if 0 <= num < 9:
                self.__list[i] = num
            else:
                del self.__list
                raise Exception('argument out of range')
        self.history = []

    def __str__(self):
        format_str = '\n+---+---+---+\n| {} | {} | {} |' * 3 + '\n+---+---+---+\n'
        return format_str.format(*self.tuple)

    def __eq__(self, other):
        return self.__list == other.__list

    def __swap(self, i, j):
        self.__list[i], self.__list[j] = self.__list[j], self.__list[i]

    @property
    def tuple(self):
        temp_list = [0] * 9
        for i, num in enumerate(self.__list):
            temp_list[i] = num if num != 0 else ' '
        return tuple(temp_list)

    @property
    def copy(self):
        copy = Puzzle(*self.__list)
        copy.history = [*self.history]
        return copy

    @property
    def clear_copy(self):
        return Puzzle(*self.__list)

    @property
    def step(self):
        return len(self.history)

    @property
    def actions(self):
        actions = set()
        for action in Puzzle.action_set:
            if self.can_move(action):
                actions.add(action)
        return actions

    @staticmethod
    def random_puzzle():
        raw_list = [x for x in range(9)]
        random_list = []
        while len(raw_list) > 0:
            random_list.append(raw_list.pop(random.randint(0, len(raw_list) - 1)))
        return Puzzle(*random_list)

    def position(self, num):
        if not 0 <= num < 9:
            raise Exception("cannot check position for {}".format(num))
        index = self.__list.index(num)
        return index // 3, index % 3

    def can_move(self, action):
        return self.position(0)[0] + action.row in range(0, 3) and \
            self.position(0)[1] + action.col in range(0, 3)

    def move(self, *actions):
        for action in actions:
            if self.can_move(action):
                pos = self.__list.index(0)
                new_pos = pos + action.raw
                self.__swap(pos, new_pos)
                self.history.append(action)

    def shuffle(self, times):
        for _ in range(times):
            actions = [*self.actions]
            self.move(actions[random.randint(0, len(actions) - 1)])

    def undo(self, steps):
        if steps == 0:
            return
        pos = self.__list.index(0)
        old_pos = pos - self.history.pop(-1).raw
        self.__swap(pos, old_pos)
        self.undo(steps - 1)

    def heuristic(self, goal):
        dist = 0
        for i in range(1, 9):
            dist += abs(self.position(i)[0] - goal.position(i)[0])
            dist += abs(self.position(i)[1] - goal.position(i)[1])
        return dist


class Problem:

    # initial_state: Puzzle
    # goal_state: Puzzle
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state.clear_copy
        self.goal_state = goal_state.clear_copy

    # state: Puzzle
    @classmethod
    def actions(cls, state):
        return state.actions

    # state: Puzzle
    # action: Puzzle.Action
    @classmethod
    def result(cls, state, action):
        copy = state.copy
        copy.move(action)
        return copy

    # state: Puzzle
    def goal_test(self, state):
        return state == self.goal_state


class Node:

    # problem: Problem
    # parent: Node
    # action: Puzzle.Action
    def __init__(self, problem, parent=None, action=None):
        self.state = problem.initial_state if parent is None else problem.result(parent.state, action)
        self.parent = parent

    @property
    def action(self):
        return self.solution[-1]

    @property
    def cost(self):
        return len(self.solution)

    @property
    def solution(self):
        return self.state.history


class LIFOQueue:

    def __init__(self):
        self.__list = []

    @property
    def empty(self):
        return len(self.__list) == 0

    # item: Node
    def insert(self, item):
        self.__list.insert(0, item)

    def pop(self):
        self.__list.pop(0)


class TreeSearch:

    class Failure:

        def __init__(self, message='Unknown Error'):
            self.message = message

        def __repr__(self):
            return '<Failure>'

        def __str__(self):
            return '<Tree Search Failure: {}>'.format(self.message)

    class Cutoff:

        def __init__(self, depth=None):
            self.depth = depth

        def __repr__(self):
            return '<Cutoff>'

        def __str__(self):
            return '<Tree Search Cutoff: Depth {}>'.format(self.depth)

    IDDFS_threshold = 13

    def __init__(self, problem):
        self.problem = problem

    # private member
    def __recursive_search(self, node, limit):
        if self.problem.goal_test(node.state):
            return node.solution
        elif limit == 0:
            return TreeSearch.Cutoff(limit)
        else:
            cutoff_occurred = False
            for action in self.problem.actions(node.state):
                child = Node(self.problem, node, action)
                result = self.__recursive_search(child, limit - 1)
                if type(result) is TreeSearch.Cutoff:
                    cutoff_occurred = True
                elif type(result) is not TreeSearch.Failure:
                    return result
            if cutoff_occurred:
                return TreeSearch.Cutoff(limit)
            else:
                return TreeSearch.Failure()

    def depth_limited_search(self, limit):
        return self.__recursive_search(Node(self.problem), limit)

    def iterative_deepening_search(self):
        for depth in range(TreeSearch.IDDFS_threshold + 1):
            print('Depth {}: '.format(depth), end='')
            result = self.depth_limited_search(depth)
            if type(result) is not TreeSearch.Cutoff:
                print('Solution found!')
                return result
            else:
                print('Not found...')
        print('No solution found within depth {}. Search failure!'.format(TreeSearch.IDDFS_threshold))
        return TreeSearch.Cutoff(TreeSearch.IDDFS_threshold)

    def __iterative_search(self, strategy):
        pass

