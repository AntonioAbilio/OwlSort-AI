class GameState:
    def __init__(self, branches, move_history=None):
        self.branches = branches
        self.move_history = move_history if move_history is not None else []
        
    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        if len(self.branches) != len(other.branches):
            return False
        for i in range(len(self.branches)):
            if not self.branches[i] == other.branches[i]:
                return False
        return True
    
    def __hash__(self):
        # Create a hashable representation of the state
        state_tuple = tuple(tuple((bird.color) for bird in branch.birds) for branch in self.branches)
        return hash(state_tuple)
    
    def print_state(self):
        """Print the current state for debugging"""
        print("GameState:")
        for i, branch in enumerate(self.branches):
            birds_colors = [f"{bird.color}" for bird in branch.birds]
            print(f"  Branch {i}: {birds_colors}")