from algorithms import algo_utils
from utils.utilities import *
import heapq
import time

def find_solution(game_state, cancel_event):
    start_time = time.time()
    
    # In greedy best-first search, we only use the heuristic value
    # No consideration of path cost
    queue = [(algo_utils.evaluate_state(game_state), id(game_state), game_state, [])]
    starting_memory_usage = process_memory()
    heapq.heapify(queue)
   
    # Track visited states so we don't repeat
    visited = set([hash(game_state)])
    states_checked = 0
   
    while queue:
        current_memory_usage = process_memory()
        if cancel_event.is_set():
            return []

        states_checked += 1
       
        # Get state with lowest heuristic value
        _, _, current_state, current_path = heapq.heappop(queue)
       
        if current_state.is_solved():
            end_time = time.time()
            elapsed_time = end_time - start_time
            print_statistics(current_path, "Greedy", states_checked, elapsed_time, current_memory_usage, starting_memory_usage, True)
            return current_path
       
        # Expand creates a list of all possible states from current state and the move to get there
        for new_state, from_idx, to_idx in algo_utils.expand_states(current_state):
            new_path = current_path + [(from_idx, to_idx)]
           
            # Check if repetition
            new_state_hash = hash(new_state)
            if new_state_hash not in visited:
                visited.add(new_state_hash)
               
                # For greedy best-first search, priority is ONLY the heuristic value
                priority = algo_utils.evaluate_state(new_state)
                heapq.heappush(queue, (priority, id(new_state), new_state, new_path))
   
    end_time = time.time()
    elapsed_time = end_time - start_time
    print_statistics(elapsed_time=elapsed_time, solutionFound=False)
    return []