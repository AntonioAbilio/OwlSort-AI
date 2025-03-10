from algorithms import algo_utils, tree_node
from states.gameState import GameState

#################################################################
#                      Depth limited Search                     #
#################################################################
# https://www.geeksforgeeks.org/depth-limited-search-for-ai/    #
#################################################################
def find_solution(self, maxDepth=16): # TODO: Might need to change maxDepth
	goal = depth_limited_search(tree_node.TreeNode(GameState(self.branches)), 0, 0, [], maxDepth)
	path = tree_node.trace_path(goal)
	path = [(p[0], p[1]) for p in path[1:]]
	if goal == None:
	 	print("No solution found!")
	else:
	    tree_node.trace_path(goal)
	return path  

def depth_limited_search(initial_node, goal_state_func, operators_func, visited, depth_limit):
    if initial_node in visited:  
        return None  # Avoid cycles
    
    visited.append(initial_node)  # Mark state as visited 
    
    if initial_node.state.is_solved():   # check goal state
        print("Goal state found!")
        return initial_node
    elif depth_limit == 0:
        return None    
    else:
        for (state, from_idx, to_idx) in algo_utils.expand_states(initial_node.state):   # go through next states
            # create tree node with the new state
            child = tree_node.TreeNode(state, from_idx, to_idx, initial_node)
            child.set_parent(initial_node)
            initial_node.add_child(child)
                    
            result = depth_limited_search(child, goal_state_func, operators_func, visited, depth_limit-1)
            if result:  # If a solution was found, return it immediately
                return result  
    return None
