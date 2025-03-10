from algorithms import dls, tree_node
from states.gameState import GameState

#################################################################
#                   Iterative Deepening Search                  #
#################################################################
def find_solution(self, maxDepth=16): # TODO: Might need to change maxDepth
	goal = iterative_deepening_search(tree_node.TreeNode(GameState(self.branches)), 0, 0, maxDepth)
	path = tree_node.trace_path(goal)
	path = [(p[0], p[1]) for p in path[1:]]
	if goal == None:
	 	print("No solution found!")
	else:
	    tree_node.trace_path(goal)
	return path

def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
    for i in range(1, depth_limit+1):
        goal = dls.depth_limited_search(initial_state, goal_state_func, operators_func, [], i)
        if goal != None:
            return goal
    return None
