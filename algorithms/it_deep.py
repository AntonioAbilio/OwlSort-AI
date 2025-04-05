from algorithms import dls, tree_node
from states.gameState import GameState
from utils.utilities import *
import time

#################################################################
#                   Iterative Deepening Search                  #
#################################################################
start_time = time.time()

def find_solution(self, cancel_event, maxDepth=16): # TODO: Might need to change maxDepth
	start_time = time.time()
    
	starting_memory_usage = process_memory()
	# Element in idx 0 is for keeping track of the memory currently consumed by the program.
    # Element in idx 1 is for keeping track of the number of states that we visit.
	arrayRef = [0, 0]
	goal = iterative_deepening_search(tree_node.TreeNode(GameState(self.branches, isMock=True)), 0, 0, maxDepth, start_time, cancel_event, arrayRef)
	path = tree_node.trace_path(goal)
	path = [(p[0], p[1]) for p in path[1:]]
	solutionFound = goal != None

	if solutionFound:
		tree_node.trace_path(goal)
    
	end_time = time.time()
	elapsed_time = end_time - start_time
	print_statistics(path, "ItDeep", arrayRef[1], elapsed_time, arrayRef[0], starting_memory_usage, solutionFound)
	return path 

def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit, start_time, cancel_event, arrayRef):
	arrayRef[0] = process_memory()
	arrayRef[1] += 1
	for i in range(1, depth_limit+1):
		if cancel_event.is_set():
			return None
		
		print(f"Searching with depth limit {i}")

		goal = dls.depth_limited_search(initial_state, goal_state_func, operators_func, [], i, start_time, cancel_event, arrayRef)
		if goal != None:
			return goal
		

	return None
