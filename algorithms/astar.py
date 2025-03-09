from algorithms import algo_utils
from states.gameState import GameState
import heapq


def find_solution(game_state):

    queue = [(algo_utils.evaluate_state(game_state), id(game_state), game_state, [])]
    heapq.heapify(queue)
    
    # Track visited states
    visited = set([hash(game_state)])
    states_checked = 0
    
    while queue:
        states_checked += 1
        if states_checked % 100 == 0:
            print(f"A* progress: {states_checked} states checked, queue size: {len(queue)}")
        
        # Get state with lowest evaluation score
        _, _, current_state, current_path = heapq.heappop(queue)
        
        # Check if this is a winning state
        if current_state.is_solved():
            print(f"Solution found! Path length: {len(current_path)}")
            print(f"A* stats: {states_checked} states checked")
            return current_path
        
        # Skip deadlock states
        #if algo_utils.is_deadlock(current_state):
        #    continue
        
        # Expand this state
        for new_state, from_idx, to_idx in algo_utils.expand_states(current_state):
            new_path = current_path + [(from_idx, to_idx)]
            
            # Check if we've seen this state before
            new_state_hash = hash(new_state)
            if new_state_hash not in visited:
                visited.add(new_state_hash)
                
                # Calculate priority and add to queue
                priority = algo_utils.evaluate_state(new_state)
                heapq.heappush(queue, (priority, id(new_state), new_state, new_path))
    
    print("No solution found")
    return []