from algorithms import algo_utils
from collections import deque
from states.gameState import GameState
from algorithms import algo_utils
import time

def find_solution(game_state, max_depth=-1):
    """
    Use Depth-First Search to find a solution path.
    
    Parameters:
    game_state - The initial GameState
    max_depth - Maximum search depth, -1 for unlimited
    
    Returns:
    A list of moves [(from_idx, to_idx), ...] representing the solution path
    """
    import sys
    
    start_time = time.time()
    print(f"\n=== Finding solution with DFS (maxDepth={max_depth}) ===")
    
    # Check if already solved
    if game_state.is_solved():
        print("Game is already solved!")
        return []
   
    # Setup for DFS
    stack = [(game_state, [], 0)]  # (state, move_path, depth)
    visited = set([hash(game_state)])  # Use hash to track visited states
    best_solution = None
    best_solution_length = sys.maxsize
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
            # Found a solution
            if len(current_path) < best_solution_length:
                print(f"New solution found! Path length: {len(current_path)}")
                if best_solution:
                    print(f"Previous best was: {best_solution_length}")
                best_solution = current_path
                best_solution_length = len(current_path)
            continue
       
        # Stop exploring if we've reached the maximum depth
        if max_depth != -1 and current_depth >= max_depth:
            continue
       
        # Expand this state (reversed order for DFS to prioritize first branches)
        next_states = algo_utils.expand_states(current_state)
        for new_state, from_idx, to_idx in reversed(next_states):
            new_path = current_path + [(from_idx, to_idx)]
            new_state_hash = hash(new_state)
            
            if new_state_hash not in visited:
                visited.add(new_state_hash)
                stack.append((new_state, new_path, current_depth + 1))
   
    # Report results
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\nDFS search completed:")
    print(f"States checked: {states_checked}")
    print(f"Max stack size: {max_stack_size}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    
    if best_solution:
        print(f"Best solution has {len(best_solution)} moves")
    else:
        print(f"No solution found within depth limit {max_depth}")
   
    return best_solution or []