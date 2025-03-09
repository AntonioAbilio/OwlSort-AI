from states.gameState import GameState

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