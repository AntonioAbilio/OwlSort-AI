import sys
from collections import deque
import time
from algorithms import algo_utils
import heapq

def find_solution(self, cancel_event):
    """Use Dijkstra's Algorithm to find the shortest solution path."""
    start_time = time.time()

    start_state = self.clone()
    
    # Dictionary to store visited states and their costs
    visited = {}
    
    # Priority queue for uniform cost search [(cost, state_hash, state, path)]
    priority_queue = []
    
    # Add start state to the queue with cost 0
    heapq.heappush(priority_queue, (0, hash(start_state), start_state, []))
    
    # Dictionary to track the best path to each state
    best_paths = {hash(start_state): []}
    
    # Best solution path found
    best_path = None
    
    nodes_explored = 0
    
    while priority_queue and not cancel_event.is_set():
        # Get state with lowest cost from the priority queue
        current_cost, current_hash, current_state, path_so_far = heapq.heappop(priority_queue)
        nodes_explored += 1
        
        # Skip if we've already found a better path to this state
        if current_hash in visited and visited[current_hash] < current_cost:
            continue
            
        # Mark this state as visited with its cost
        visited[current_hash] = current_cost
        
        # Check if this is a winning state
        if current_state.is_solved():
            best_path = path_so_far
            break
            
        # Generate successor states
        for new_state, from_idx, to_idx in algo_utils.expand_states(current_state):
            new_hash = hash(new_state)
            
            # Cost is the number of moves (each move costs 1)
            new_cost = current_cost + 1
            
            # Skip if we've already found a better path to this state
            if new_hash in visited and visited[new_hash] <= new_cost:
                continue
                
            # Create a new path by appending the current move
            new_path = path_so_far + [(from_idx, to_idx)]
            
            # Update the best path to this state
            best_paths[new_hash] = new_path
            
            # Add new state to the priority queue
            heapq.heappush(priority_queue, (new_cost, new_hash, new_state, new_path))
    
    if best_path:
        print(f"Best solution has {len(best_path)} moves")
    else:
        print("No solution found")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.5f} seconds")
    print(f"Nodes explored: {nodes_explored}")
    
    if best_path:
        return deque(best_path)
    else:
        return deque([])