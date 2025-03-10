from states.gameState import GameState
from constants import COLORS, MAX_BIRDS_PER_BRANCH

def expand_states(game_state):
    assert isinstance(game_state, GameState)
    next_states = []
    
    for from_idx in range(len(game_state.branches)):
        for to_idx in range(len(game_state.branches)):
            if from_idx == to_idx:
                continue
            
            new_state = game_state.clone()
            
            if new_state.apply_move(from_idx, to_idx):
                next_states.append((new_state, from_idx, to_idx))
    return next_states

def evaluate_state(game_state): #calculate euristic distance to solution (lower better)
    assert isinstance(game_state, GameState)
    score = 0
    
    #completed branches are amazing for solve
    completed_count = 0
    for branch in game_state.branches:
        if len(branch.birds) == MAX_BIRDS_PER_BRANCH:
            if all(bird.color == branch.birds[0].color for bird in branch.birds):
                completed_count += 1
    
    score -= completed_count * 100
    
    #same color together good
    for branch in game_state.branches:
        if not branch.birds:
            continue
            
        color_counts = {}
        for bird in branch.birds:
            color_counts[bird.color] = color_counts.get(bird.color, 0) + 1
        
        for count in color_counts.items():
            if count[1] > 1:
                score -= (count[1] * count[1])  #square cause this is really good
    
    #longer solution is worse
    score += game_state.get_number_of_moves() * 0.5
    
    return score

def is_deadlock(game_state):
    assert isinstance(game_state, GameState)
    # If there are no moves possible, it's a deadlock
    if not expand_states(game_state):
        return True
    
    # Check if any color has birds spread across more branches than can be combined
    color_branch_count = {color: 0 for color in COLORS}
    
    for branch in game_state.branches:
        branch_colors = set()
        for bird in branch.birds:
            branch_colors.add(bird.color)
        
        for color in branch_colors:
            color_branch_count[color] += 1
    
    # If any color is spread across more than 2 branches, 
    # it might be impossible to combine them all
    for color, count in color_branch_count.items():
        if count > 2:
            return True
    
    return False