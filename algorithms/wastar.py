from algorithms import algo_utils
from utils.utilities import *
import heapq
import time

def find_solution(game_state, cancel_event, weight=5.5): #TODO: Might need to change weight


    start_time = time.time()
    
    g_score = 0 #g_score is the cost from start to current node
    h_score = algo_utils.evaluate_state(game_state) #h_score is the overall cost from current node to goal
    

    queue = [(g_score + weight * h_score, id(game_state), game_state, [], g_score)]
    heapq.heapify(queue)
   

    visited = set([hash(game_state)])
    states_checked = 0
   
    starting_memory_usage = process_memory()
    current_memory_usage = 0
    
    while queue:
        current_memory_usage = process_memory()
        if cancel_event.is_set():
            return []
        
        states_checked += 1
       
        _, _, current_state, current_path, current_g = heapq.heappop(queue)
       
        if current_state.is_solved():
            end_time = time.time()
            elapsed_time = end_time - start_time
            print_statistics(current_path, "Weighted A*", states_checked, elapsed_time, current_memory_usage, starting_memory_usage, True)
            return current_path
       
        for new_state, from_idx, to_idx in algo_utils.expand_states(current_state):
            new_path = current_path + [(from_idx, to_idx)]
            
            new_g = current_g + 0.5
            
            new_state_hash = hash(new_state)
            if new_state_hash not in visited:
                visited.add(new_state_hash)
                
                h_score = algo_utils.evaluate_state(new_state)
                
                f_score = new_g + weight * h_score
                
                heapq.heappush(queue, (f_score, id(new_state), new_state, new_path, new_g))
   
    end_time = time.time()
    elapsed_time = end_time - start_time
    print_statistics(elapsed_time=elapsed_time, solutionFound = False)
    return []