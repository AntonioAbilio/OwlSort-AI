from algorithms import algo_utils
from utils.utilities import *
from collections import deque
import time

def find_solution(game_state, cancel_event, max_depth=-1):
    """
    Use Breadth-First Search to find a solution path.

    Parameters:
    game_state - The initial GameState
    max_depth - Maximum search depth, -1 for unlimited
    
    Returns:
    A list of moves [(from_idx, to_idx), ...] representing the solution path
    """
    
    start_time = time.time()
    print(f"\n=== Finding solution with BFS (maxDepth={max_depth}) ===")
    
    # Check if already solved
    if game_state.is_solved():
        print("Game is already solved!")
        return []
    
    # Setup for BFS - use deque instead of list for efficient queue operations
    queue = deque([(game_state, [], 0)])  # (state, move_path, depth)
    visited = set([hash(game_state)])  # Use hash to track visited states
    starting_memory_usage = process_memory()
    current_memory_usage = 0
    states_checked = 0
    max_queue_size = 1
    
    while queue:
        current_memory_usage = process_memory()

        if cancel_event.is_set():
            return []
        
        states_checked += 1
        
        max_queue_size = max(max_queue_size, len(queue))
        current_state, current_path, current_depth = queue.popleft()  # Use popleft() for FIFO behavior
        
        # Check if this is a winning state
        if current_state.is_solved():
            # BFS guarantees the first solution found is the shortest
            print(f"Solution found! Path length: {len(current_path)}")
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            """ print(f"\nBFS search completed:")
            print(f"States checked: {states_checked}")
            print(f"Max queue size: {max_queue_size}")
            print(f"Time taken: {elapsed_time:.2f} seconds") """

            print_statistics(current_path, "BFS", states_checked, elapsed_time, current_memory_usage, starting_memory_usage, True)
            
            return current_path
        
        # Stop exploring if we've reached the maximum depth
        if max_depth != -1 and current_depth >= max_depth:
            continue
        
        # Expand this state
        next_states = algo_utils.expand_states(current_state)
        for new_state, from_idx, to_idx in next_states:
            new_path = current_path + [(from_idx, to_idx)]
            new_state_hash = hash(new_state)
            
            if new_state_hash not in visited:
                visited.add(new_state_hash)
                queue.append((new_state, new_path, current_depth + 1))
    
    # If we get here, no solution was found
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\nBFS search completed:")
    print_statistics(solutionFound = False)
    """ print(f"States checked: {states_checked}")
    print(f"Max queue size: {max_queue_size}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"No solution found within depth limit {max_depth}") """
    
    return []