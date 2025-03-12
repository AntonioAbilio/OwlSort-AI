from states.gameState import GameState


#cached_solutions = {
#    First game state (hash: 12345)
#    12345: {
#        Algorithm.BFS: [(0, 2), (1, 3), (0, 1)],  BFS solution path
#        Algorithm.DFS: [(0, 1), (2, 3), (0, 2)],  DFS solution path
#        Algorithm.ASTAR: [(0, 2), (1, 0), (3, 1)] A* solution path
#    },
#   ...
#}
class SolutionCache:
    def __init__(self):
        self.cached_solutions = {}  # Dictionary to store solutions by algorithm
        self.current_state_hash = None
        self.current_algorithm = None
    
    def get_solution(self, game_state, algorithm):
        state_hash = hash(game_state)
        
        # Check if we have a cached solution for this state and algorithm
        if state_hash in self.cached_solutions and algorithm in self.cached_solutions[state_hash]:

            path = self.cached_solutions[state_hash][algorithm]
            from_idx, to_idx = path[0]
            if not(game_state.is_valid_move(from_idx, to_idx)):
                return None
            return path
        
        return None
    
    def store_solution(self, game_state, algorithm, solution):
        state_hash = hash(game_state)
        
        if state_hash not in self.cached_solutions:
            self.cached_solutions[state_hash] = {}
            
        self.cached_solutions[state_hash][algorithm] = solution
        self.current_state_hash = state_hash
        self.current_algorithm = algorithm
    
    def update_after_move(self, game_state, move):
        if self.current_state_hash is None or self.current_algorithm is None:
            return False
            
        # Get the current solution
        previous_state_hash = self.current_state_hash
        algorithm = self.current_algorithm
        
        if previous_state_hash in self.cached_solutions and algorithm in self.cached_solutions[previous_state_hash]:
            solution = self.cached_solutions[previous_state_hash][algorithm]
            
            # Check if user's move matches the first move in the solution
            if solution and len(solution) > 0 and solution[0] == move:
                # Remove the first move from the solution
                updated_solution = solution[1:]
                
                # Store the updated solution for the new state
                new_state_hash = hash(game_state)
                if new_state_hash not in self.cached_solutions:
                    self.cached_solutions[new_state_hash] = {}
                    
                self.cached_solutions[new_state_hash][algorithm] = updated_solution
                self.current_state_hash = new_state_hash
                
                return True
                
        return False