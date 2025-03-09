import sys
from collections import deque
from states.gameState import GameState

from algorithms import algo_utils

def find_solution(self, maxDepth = -1):
    """Use DFS to find a solution path."""
    print(f"\n=== Finding solution with DFS (maxDepth={maxDepth}) ===")
    if self.solution_path:
        print("Using existing solution path")
        return self.solution_path
   
    # Create a starting state using the game's current state
    current_game_state = self.get_game_state()
    if (current_game_state.is_solved()):
        print("Game is already solved!")
        return self.solution_path
   
    # Setup for DFS
    stack = [(current_game_state, deque(), 0)]  # (state, move_path, depth)
    visited = set([hash(current_game_state)])  # Use hash to track visited states
    old_path = []
    old_path_size = sys.maxsize
    states_checked = 0
    max_stack_size = 1
   
    while stack:
        states_checked += 1
        if states_checked % 100 == 0:
            print(f"DFS progress: {states_checked} states checked, stack size: {len(stack)}")
       
        max_stack_size = max(max_stack_size, len(stack))
        current_state, current_path, current_depth = stack.pop()
       
        # Check if this is a winning state
        if current_state.is_solved():
            print(f"Solution found! Path length: {len(current_path)}")
            print(f"DFS stats: {states_checked} states checked, max stack size: {max_stack_size}")
           
            if len(current_path) < old_path_size:
                print("Found new path, old was ", old_path, " and new is ", current_path)
                old_path = current_path
                old_path_size = len(current_path)
            continue
       
        # Stop exploring if we've reached the maximum depth
        if maxDepth != -1 and current_depth >= maxDepth:
            continue
       
        #use expand_states to generate all possible next states
        for new_state, from_idx, to_idx in algo_utils.expand_states(current_state):
            new_path = current_path + deque([(from_idx, to_idx)])

            new_state_hash = hash(new_state)
            if new_state_hash not in visited:
                visited.add(new_state_hash)
                stack.append((new_state, new_path, current_depth + 1))
   
    if old_path:
        print(f"Best solution has {len(old_path)} moves")
    else:
        print(f"No solution found within depth limit {maxDepth}")
   
    return old_path