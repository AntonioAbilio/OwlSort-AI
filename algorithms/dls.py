from algorithms import algo_utils, tree_node
from states.gameState import GameState
from utils.utilities import *
import time

#################################################################
#                      Depth limited Search                     #
#################################################################
# https://www.geeksforgeeks.org/depth-limited-search-for-ai/    #
#################################################################
def find_solution(self, cancel_event, maxDepth=16): # TODO: Might need to change maxDepth
    start_time = time.time()

    starting_memory_usage = process_memory()
    # Element in idx 0 is for keeping track of the memory currently consumed by the program.
    # Element in idx 1 is for keeping track of the number of states that we visit.
    arrayRef = [0, 0]
    goal = depth_limited_search(tree_node.TreeNode(GameState(self.branches, isMock=True)), 0, 0, [], maxDepth, start_time, cancel_event, arrayRef)
    path = tree_node.trace_path(goal)
    path = [(p[0], p[1]) for p in path[1:]]
    
    solutionFound = goal != None

    if solutionFound:
        tree_node.trace_path(goal)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print_statistics(path, "DLS", arrayRef[1], elapsed_time, arrayRef[0], starting_memory_usage, solutionFound)
    return path  

def depth_limited_search(initial_node, goal_state_func, operators_func, visited, depth_limit, start_time, cancel_event, arrayRef):
    arrayRef[0] = process_memory()
    arrayRef[1] += 1
    if cancel_event.is_set():
        return None
        
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
                    
            result = depth_limited_search(child, goal_state_func, operators_func, visited, depth_limit-1, start_time, cancel_event, arrayRef)  
            if result:  # If a solution was found, return it immediately
                return result  
    return None
