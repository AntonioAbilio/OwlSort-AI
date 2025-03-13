from algorithms import algo_utils
import heapq
import time

def find_solution(game_state):
    start_time = time.time()
    
    # In greedy best-first search, we only use the heuristic value
    # No consideration of path cost
    queue = [(algo_utils.evaluate_state(game_state), id(game_state), game_state, [])]
    heapq.heapify(queue)
   
    # Track visited states so we don't repeat
    visited = set([hash(game_state)])
    states_checked = 0
   
    while queue:
        states_checked += 1
       
        # Get state with lowest heuristic value
        _, _, current_state, current_path = heapq.heappop(queue)
       
        if current_state.is_solved():
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Solution found! Path length: {len(current_path)}")
            print(f"Greedy Best-First Search stats: {states_checked} states checked")
            print(f"Time taken: {elapsed_time:.5f} seconds")
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
    print("No solution found")
    print(f"Time taken: {elapsed_time:.5f} seconds")
    return []