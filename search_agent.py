class ProblemFormulation:

    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    @classmethod
    def actions(cls, state):
        raise NotImplementedError

    @classmethod
    def result(cls, state, action):
        raise NotImplementedError

    def heuristic(self, state):
        raise NotImplementedError

    def goal_test(self, state):
        raise NotImplementedError


class SearchAgent:

    # abstract class
    class PriorityQueue:

        def __init__(self, *args):
            self.__list = [*args]

        def __contains__(self, item):
            exist = False
            for node in self.__list:
                if item.state == node.state:
                    exist = True
            return exist

        def __lshift__(self, other):
            self.__list.insert(0, other)

        @classmethod
        def compare(cls, item1, item2):
            raise NotImplementedError

        @property
        def empty(self):
            return len(self.__list) == 0

        def pop(self):
            best = None
            for node in self.__list:
                best = node if best is None else self.compare(node, best)
            self.__list.remove(best)
            return best

        def try_replace(self, item):
            replaced = False
            for node in self.__list:
                if item.state == node.state and self.compare(item, node) is item:
                    self.__list.remove(node)
                    self << item
                    replaced = True
            return replaced

    class ExploredSet:

        def __init__(self, *args):
            self.__set = {*args}

        def __contains__(self, item):
            exist = False
            for node in self.__set:
                if item.state == node.state:
                    exist = True
            return exist

        def __lshift__(self, other):
            self.__set.add(other)

    class Node:

        # problem: Problem
        # parent: Node
        # action: Puzzle.Action
        def __init__(self, problem, parent=None, action=None):
            self.state = problem.initial_state if parent is None else problem.result(parent.state, action)
            self.cost = 0 if parent is None else parent.cost + action.cost
            self.parent = parent
            self.action = action
            self.heuristic = problem.heuristic(self.state)

        @property
        def solution(self):
            solution = [] if self.parent is None else self.parent.solution + [self.action]
            if solution is None:
                raise Exception('solution is none')
            return solution

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

    IDDFS_threshold = 20

    def __init__(self, problem):
        if not issubclass(type(problem), ProblemFormulation):
            raise TypeError('Subclass of ProblemFormulation expected!')
        self.problem = problem

    # private member
    def __recursive_tree_search(self, node, limit):
        if self.problem.goal_test(node.state):
            return node.solution
        elif limit == 0:
            return SearchAgent.Cutoff(limit)
        else:
            cutoff_occurred = False
            for action in self.problem.actions(node.state):
                child = SearchAgent.Node(self.problem, node, action)
                result = self.__recursive_tree_search(child, limit - 1)
                if type(result) is SearchAgent.Cutoff:
                    cutoff_occurred = True
                elif type(result) is not SearchAgent.Failure:
                    return result
            if cutoff_occurred:
                return SearchAgent.Cutoff(limit)
            else:
                return SearchAgent.Failure()

    # private member
    def __iterative_graph_search(self, queue_type):
        node = SearchAgent.Node(self.problem)
        frontier = queue_type(node)
        explored = SearchAgent.ExploredSet()
        while True:
            if frontier.empty:
                return SearchAgent.Failure('Solution do not exist!')
            node = frontier.pop()
            if self.problem.goal_test(node.state):
                return node.solution
            explored << node
            for action in self.problem.actions(node.state):
                child = SearchAgent.Node(self.problem, node, action)
                if child not in frontier and child not in explored:
                    frontier << child
                else:
                    frontier.try_replace(child)

    def depth_limited_search(self, limit):
        return self.__recursive_tree_search(SearchAgent.Node(self.problem), limit)

    def iterative_deepening_search(self):
        for depth in range(SearchAgent.IDDFS_threshold + 1):
            print('Depth {}: '.format(depth), end='')
            result = self.depth_limited_search(depth)
            if type(result) is not SearchAgent.Cutoff:
                print('Solution found!')
                return result
            else:
                print('Not found...')
        print('No solution found within depth {}. Search failure!'.format(SearchAgent.IDDFS_threshold))
        return SearchAgent.Cutoff(SearchAgent.IDDFS_threshold)

    def a_star_search(self):
        class AStarPriorityQueue(SearchAgent.PriorityQueue):
            @classmethod
            def compare(cls, item1, item2):
                return item1 if item1.cost + item1.heuristic < item2.cost + item2.heuristic else item2
        return self.__iterative_graph_search(AStarPriorityQueue)
