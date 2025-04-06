from states.gameState import GameState
from global_vars import Globals
import math

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

def evaluate_state(game_state):
    assert isinstance(game_state, GameState)
    
    unsorted_branches = 0
    completed_branches = 0
    for branch in game_state.branches:
        if not branch.birds:
            continue
        if len(branch.birds) == Globals.MAX_BIRDS_PER_BRANCH and all(bird.color == branch.birds[0].color for bird in branch.birds):
            completed_branches += 1
        else:
            unsorted_branches += 1

    color_group_counts = {}
    for branch in game_state.branches:
        if not branch.birds:
            continue
        current_color = None
        for bird in branch.birds:
            if bird.color != current_color:
                current_color = bird.color
                color_group_counts[current_color] = color_group_counts.get(current_color, 0) + 1

    merge_moves = sum((count - 1) for count in color_group_counts.values() if count > 0)
    branch_solve_moves = math.ceil(unsorted_branches/2)
    
    heuristic_lower_bound = max(branch_solve_moves, merge_moves)



    return heuristic_lower_bound #+ move_penalty


def is_deadlock(game_state):
    assert isinstance(game_state, GameState)
    # If there are no moves possible, it's a deadlock
    if not expand_states(game_state):
        return True
    
    # Check if any color has birds spread across more branches than can be combined
    color_branch_count = {color: 0 for color in Globals.COLORS}
    
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