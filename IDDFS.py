from puzzle import Puzzle
from search_tree import SearchTree


def Recursive_DLS(node,search_tree,limit):
    if node.state==search_tree.goal:
        return SearchTree.history
    else if limit == 0:
        return SearchTree.cutoff
    else:
        cutoff_occurred=False
        for action in Puzzle.actions:
            if frontier.state.can_move(action):
                child_state = frontier.copy
                child_state.move(action)
                child_node = search_tree.__make_node(child_state, frontier, action, frontier.depth + 1)
                search_tree.add_frontier(child_node)
                if result==cutoff:
                    cutoff_occurred=True
                else if result != failure:
                    return result
        if cutoff_occurred:
            return cutoff
        else:
            return failure

def Depth_Limited_Search(search_tree,depth):
    return Recursive_DLS(search_tree.initial,search_tree,depth)

def Iterative_Deepening_Search(search_tree):
    for depth in range(0, 20):
        result=Depth_Limited_Search(search_tree,depth)
        if result != cutoff:
            return result
    
initial_state = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
goal_state = Puzzle(1, 2, 0, 3, 4, 5, 6, 7, 8)
search_tree = SearchTree(initial_state, goal_state)

