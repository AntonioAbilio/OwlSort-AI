class GameState:
    def __init__(self, branches, move_history=None):
        """
        Initialize a game state object to track the state of branches and move history.
        
        Parameters:
        branches - List of Branch objects representing the current game state
        move_history - List of (from_idx, to_idx) tuples representing the sequence of moves made
        """
        self.branches = branches
        self.move_history = move_history if move_history is not None else []
       
    def __eq__(self, other):
        """
        Compare two GameState objects for equality.
        Two GameStates are equal if all their branches contain the same birds in the same order.
        """
        if not isinstance(other, GameState):
            return False
        if len(self.branches) != len(other.branches):
            return False
        for i in range(len(self.branches)):
            if not self.branches[i] == other.branches[i]:
                return False
        return True
   
    def __hash__(self):
        """
        Create a hashable representation of the state.
        This is useful for using GameState as a key in dictionaries or sets.
        """
        # Create a hashable representation of the state
        state_tuple = tuple(tuple((bird.color) for bird in branch.birds) for branch in self.branches)
        return hash(state_tuple)
   
    def print_state(self):
        """Print the current state for debugging"""
        print("GameState:")
        for i, branch in enumerate(self.branches):
            birds_colors = [f"{bird.color}" for bird in branch.birds]
            print(f"  Branch {i}: {birds_colors}")
    
    def clone(self):
        """
        Create a deep copy of this GameState.
        Useful for exploring possible future states without modifying the original.
        """
        from models.branch import Branch
        from models.bird import Bird
        
        # Clone branches
        new_branches = []
        for branch in self.branches:
            new_branch = Branch(branch.x, branch.y, branch.id)
            new_branch.side = branch.side
            new_branch.is_completed = branch.is_completed
            
            # Clone birds
            for bird in branch.birds:
                new_bird = Bird(bird.color)
                new_branch.birds.append(new_bird)
            
            new_branches.append(new_branch)
        
        # Return a new GameState with cloned branches and copied move history
        return GameState(new_branches, self.move_history.copy())
    
    def apply_move(self, from_idx, to_idx): 
        #this will try to move, if it does it updates itself and returns true, if it cant it returns false
        from_branch = self.branches[from_idx]
        to_branch = self.branches[to_idx]
        
        if not from_branch.birds or to_branch.is_completed:
            return False
        
        # Get the color of the topmost bird in the source branch
        top_bird_color = from_branch.birds[-1].color
        
        # Find all birds of the same color in sequence from the top
        birds_to_move = []
        for i in range(len(from_branch.birds) - 1, -1, -1):
            if from_branch.birds[i].color == top_bird_color:
                birds_to_move.insert(0, from_branch.birds[i])
            else:
                break
        
        # Check if target branch can accept these birds
        if not to_branch.birds:
            # Empty branch can accept any birds if there's space
            can_move = len(birds_to_move) <= (4 - len(to_branch.birds))  # Assuming MAX_BIRDS_PER_BRANCH is 4
        else:
            # Non-empty branch can only accept matching color birds if there's space
            can_move = (to_branch.birds[-1].color == top_bird_color and 
                       len(birds_to_move) <= (4 - len(to_branch.birds)))
        
        if can_move:
            # Remove birds from source branch
            for _ in range(len(birds_to_move)):
                from_branch.birds.pop()
            
            # Add birds to target branch
            for bird in birds_to_move:
                to_branch.add_bird(bird)
            
            # Record the move in the history
            self.move_history.append((from_idx, to_idx))
            
            # Check completion
            if len(to_branch.birds) == 4:  # Assuming MAX_BIRDS_PER_BRANCH is 4
                if all(bird.color == to_branch.birds[0].color for bird in to_branch.birds):
                    to_branch.is_completed = True
            

            return True
        return False
    
    def get_move_history(self):
        return self.move_history
    
    def get_number_of_moves(self):
        return self.move_history.__len__
    
    def is_solved(self):
        from constants import COLORS
        from constants import MAX_BIRDS_PER_BRANCH

        completed_count = 0
        for branch in self.branches:
            if len(branch.birds) == MAX_BIRDS_PER_BRANCH:
                if all(bird.color == branch.birds[0].color for bird in branch.birds):
                    completed_count += 1
        
        return completed_count == len(COLORS)