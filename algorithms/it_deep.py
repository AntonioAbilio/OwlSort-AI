from algorithms import dls, tree_node
from constants import ALGORITHM_TIMEOUT
from states.gameState import GameState
import time

#################################################################
#                   Iterative Deepening Search                  #
#################################################################
start_time = time.time()

def find_solution(self, maxDepth=16): # TODO: Might need to change maxDepth
	start_time = time.time()
     
	goal = iterative_deepening_search(tree_node.TreeNode(GameState(self.branches)), 0, 0, maxDepth, start_time)
	path = tree_node.trace_path(goal)
	path = [(p[0], p[1]) for p in path[1:]]
	if goal == None:
		print("No solution found!")
	else:
		tree_node.trace_path(goal)
			
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(f"Time taken: {elapsed_time:.5f} seconds")
	return path

def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit, start_time):
	for i in range(1, depth_limit+1):
		print(f"Searching with depth limit {i}")

		goal = dls.depth_limited_search(initial_state, goal_state_func, operators_func, [], i, start_time)
		if goal != None:
			return goal
		

	return None
