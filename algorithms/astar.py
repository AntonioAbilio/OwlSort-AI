from algorithms import algo_utils
from utils.utilities import *
import heapq
import time

def find_solution(game_state, cancel_event):
    start_time = time.time()

    queue = [(algo_utils.evaluate_state(game_state), id(game_state), game_state, [])]
    heapq.heapify(queue)
    
    #track visited states so we dont repeat
    visited = set([hash(game_state)])
    states_checked = 0
    
    starting_memory_usage = process_memory()
    current_memory_usage = 0
    
    while queue:
        current_memory_usage = process_memory()

        if cancel_event.is_set():
            return []
        states_checked += 1
        
        #get state with lowest evaluation score
        _, _, current_state, current_path = heapq.heappop(queue)

        if current_state.is_solved():
            end_time = time.time()
            elapsed_time = end_time - start_time
            print_statistics(current_path, "A*", states_checked, elapsed_time, current_memory_usage, starting_memory_usage, True)
            return current_path
        
        #expand creates a list of all possible states from current state and the move to get there
        for new_state, from_idx, to_idx in algo_utils.expand_states(current_state):
            new_path = current_path + [(from_idx, to_idx)]
            
            #check if repetition
            new_state_hash = hash(new_state)
            if new_state_hash not in visited:
                visited.add(new_state_hash)
                
                priority = algo_utils.evaluate_state(new_state)
                heapq.heappush(queue, (priority, id(new_state), new_state, new_path))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print_statistics(solutionFound = False)
    return []