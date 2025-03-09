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
def find_solution(self, maxDepth = -1):
        print(f"No solution found within depth limit {maxDepth}")

        return 1

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        

def depth_limited_search(initial_state, goal_state_func, operators_func, visited, depth_limit):
    if initial_state in visited:  
        return None  # Avoid cycles
    
    node = TreeNode(initial_state)   # create the root node in the search tree   
    visited.append(initial_state)  # Mark state as visited 
    
    if goal_state_func(node.state):   # check goal state
        return node
    elif depth_limit == 0:
        return None    
    else:
        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            child = TreeNode(state, parent=node)
            node.add_child(child)
                    
            result = depth_limited_search(child.state, goal_state_func, operators_func, visited, depth_limit-1)
            if result:  # If a solution was found, return it immediately
                return result  
    return None

def print_sol(goal):
    if (goal != None):
        print(goal.state)
    else:
        print("No solution found.")

b1 = Branch(0,0,0)
b1.add_bird(Bird('blue'))
b1.add_bird(Bird('yellow'))
b1.add_bird(Bird('red'))
b1.add_bird(Bird('yellow'))

b2 = Branch(0,0,1)
b2.add_bird(Bird('yellow'))
b2.add_bird(Bird('green'))
b2.add_bird(Bird('green'))
b2.add_bird(Bird('blue'))

b3 = Branch(0,0,2)
b3.add_bird(Bird('red'))
b3.add_bird(Bird('red'))
b3.add_bird(Bird('green'))
b3.add_bird(Bird('red'))

b4 = Branch(0,0,3)
b4.add_bird(Bird('blue'))
b4.add_bird(Bird('yellow'))
b4.add_bird(Bird('blue'))
b4.add_bird(Bird('green'))

b5 = Branch(0,0,4)

b6 = Branch(0,0,5)

s = GameState([b1, b2, b3, b4, b5, b6])

# Define the goal state function
def goal_func(state):
    return s.goal_branch_state(state)

# Define the operators function
def op_func(state):
    return s.child_branch_states(state)

goal = depth_limited_search(s, op_func, goal_func, [], 10)

def print_solution(node):    
    if (node.parent != None):
        print_solution(node.parent)
    GameState.print_state(node.state)
    return


if goal == None:
	print("No solution found!")
else:
	print_solution(goal)        

