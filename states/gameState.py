from models.branch import Branch
from models.bird import Bird
import constants

class GameState:
    def __init__(self, branches, move_history=None, isMock=False):
        self.branch_cap = constants.MAX_BIRDS_PER_BRANCH
        self.branches = branches
        self.isMock = isMock
        self.move_history = move_history if move_history is not None else []
        assert isinstance(self.branches, list)
        assert isinstance(self.move_history, list)
       
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
        state_tuple = tuple(tuple((bird.color) for bird in branch.birds) for branch in self.branches)
        return hash(state_tuple)
   
    def print_state(self):
        print("GameState:")
        for i, branch in enumerate(self.branches):
            birds_colors = [f"{bird.color}" for bird in branch.birds]
            print(f"  Branch {i}: {birds_colors}")
    
    def clone(self):

        new_branches = []

        for branch in self.branches:
            new_branch = Branch(branch.x, branch.y, branch.id, isMock=self.isMock)
            new_branch.side = branch.side
            new_branch.is_completed = branch.is_completed
            
            # Clone birds
            for bird in branch.birds:
                new_bird = Bird(bird.color, self.isMock)
                new_branch.birds.append(new_bird)
            
            new_branches.append(new_branch)
        
        return GameState(new_branches, self.move_history.copy(), isMock=self.isMock)
    
    def is_valid_move(self, from_idx, to_idx):
        from_branch = self.branches[from_idx]
        to_branch = self.branches[to_idx]

        # Check if we can apply the move
        if not from_branch.birds or from_branch.is_completed: # Source branch is empty or complete
            return False
        if len(to_branch.birds) >= self.branch_cap: # Destination branch is full 
            return False
        # Get the color of the topmost bird in the source branch
        top_bird_color = from_branch.birds[-1].color
        if to_branch.birds:
            if (to_branch.birds[-1].color != top_bird_color): # Top color does not match
                return False
        return (from_branch, to_branch)
    
    def apply_move(self, from_idx, to_idx): 
        '''this will try to move, if it does it updates itself and returns true, if it cant it returns false'''
        
        branchTuple = self.is_valid_move(from_idx, to_idx)

        if not(isinstance(branchTuple, tuple)):
            return False
        
        from_branch, to_branch = branchTuple
        top_bird_color = from_branch.birds[-1].color
        
        # Find all birds of the same color in sequence from the top
        birds_to_move = []
        for i in range(len(from_branch.birds) - 1, -1, -1):
            if from_branch.birds[i].color == top_bird_color:
                birds_to_move.insert(0, from_branch.birds[i])
            else:
                break
        numBirdsToBeMoved = min(self.branch_cap - len(to_branch.birds), len(birds_to_move)) 
        birds_to_move = birds_to_move[:numBirdsToBeMoved] # Remove birds that can't move
                
        # Remove birds from source branch
        for _ in range(len(birds_to_move)):
            from_branch.birds.pop()
        
        # Add birds to target branch
        for bird in birds_to_move:
            to_branch.add_bird(bird)
        
        # Record the move in the history
        self.move_history.append((from_idx, to_idx))
        
        # Check completion
        if len(to_branch.birds) == self.branch_cap:  # Assuming MAX_BIRDS_PER_BRANCH is 4
            if all(bird.color == to_branch.birds[0].color for bird in to_branch.birds):
                to_branch.is_completed = True

        return True

    
    def get_move_history(self):
        assert isinstance(self.move_history, list)
        return self.move_history
    
    def get_number_of_moves(self):
        assert isinstance(self.move_history, list)
        return len(self.move_history)

    def is_solved(self):
        completed_count = 0
        for branch in self.branches:
            if len(branch.birds) == constants.MAX_BIRDS_PER_BRANCH:
                if all(bird.color == branch.birds[0].color for bird in branch.birds):
                    completed_count += 1
        return completed_count == constants.num_colors
