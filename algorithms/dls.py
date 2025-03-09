import sys
import os
from collections import deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.branch import Branch
from models.bird import Bird
from states.gameState import GameState

#################################################################
#                      Depth limited Search                     #
#################################################################
# https://www.geeksforgeeks.org/depth-limited-search-for-ai/    #
#################################################################
def find_solution(self, maxDepth=200): # TODO: Might need to change maxDepth
	goal = depth_limited_search(TreeNode(GameState(self.branches)), 0, 0, [], maxDepth) # FIXME: This value is hardcoded (use maxDepth)
	path = trace_path(goal)
	
	path = [(p[0], p[1]) for p in path[1:]]
	p = path[0] 
	self.solution_path = path
	if goal == None:
	 	print("No solution found!")
	else:
	    trace_path(goal)
	return path

# TODO: REMOVE (This is the same as expand_states from algo_utils.py, but imports are not working for some reason)
def child_branch_states(game_state):
    assert isinstance(game_state, GameState)
    next_states = []
    
    for from_idx in range(len(game_state.branches)):
        for to_idx in range(len(game_state.branches)):
            if from_idx == to_idx:
                continue
            
            new_state = game_state.clone()
            
            if new_state.apply_move(from_idx, to_idx):
                next_states.append((new_state, from_idx, to_idx))
    return next_states
        
# A generic definition of a tree node holding a state of the problem
#TODO: Move this to a different file (imports are not working for some reason)
class TreeNode:
    def __init__(self, state, from_idx=None, to_idx=None, parent=None):
        self.state = state
        self.from_idx = from_idx
        self.to_idx = to_idx
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    
    def set_parent(self, parent_node):
        self.parent = parent_node
    
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        if (self.state != other.state):
            return False
        return True
        

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
        for (state, from_idx, to_idx) in child_branch_states(initial_node.state):   # go through next states
            # create tree node with the new state
            child = TreeNode(state, from_idx, to_idx, initial_node)
            child.set_parent(initial_node)
            initial_node.add_child(child)
                    
            result = depth_limited_search(child, goal_state_func, operators_func, visited, depth_limit-1)
            if result:  # If a solution was found, return it immediately
                return result  
    return None

def trace_path(node):
    parent = node.parent
    path = []
    while parent is not None:
        path.append((parent.from_idx, parent.to_idx, parent.state)) 
        parent = parent.parent
    else:
        print("No solution found.") 
    path.reverse()
    path.append((node.from_idx, node.to_idx, node.state))
    return path

