import sys
from collections import deque
from states.gameState import GameState
from constants import MAX_BIRDS_PER_BRANCH, COLORS
from models.bird import Bird
from models.branch import Branch

def find_best_start_branches(state):
    """An heuristic that opts to use the maximum number of contiguous birds
    as a reference point to wether or not we found a good starting branch."""

    maxContiguousBirds = 0
    best_branches = []

    branches = state.branches
    for branch_idx in range(len(branches)):

        birds = branches[branch_idx].birds[::-1] # We want to start from the front to the back of the branch.

        if len(birds) == 0: # Branch is empty
            continue

        bird_colors = list(map(lambda bird: bird.color, birds))

        firstColor = bird_colors[0] # We can only move birds that are the same color as the first one.
        contiguousBirds = 1

        for remainingColor in bird_colors[1::]: # Determine how many birds of the same color are "connected".
            if (remainingColor == firstColor):
                contiguousBirds += 1
            else:
                break # As soon as we find a bird that is a different color stop counting
        
        if (contiguousBirds > maxContiguousBirds): # The more birds that we can move the better.
            best_branches.append((branch_idx, contiguousBirds)) # Save the current best branch.

    # Sort in descending order of contiguousBirds.
    best_branches.sort(key=lambda x: x[1], reverse=True)

    return [branch_tuple[0] for branch_tuple in best_branches] # Return only branch indexes.

def find_best_ending_branches(state):
    """An heuristic that opts to order branches by the amount of birds that they can still hold"""

    # TODO: Finish
    # Best case: First bird has matching color and the branches have little birds
    # Meh case: First bird has matching color
    # Worst case: Branch is empty


    branches = state.branches
    best_branches = []

    for branch_idx in range(len(branches)):
        bird_count = len(branches[branch_idx].birds)
        best_branches.append((branch_idx, bird_count))

    # Sort in ascending order of bird_count.
    # This means that branches with less birds (therefor more space) will be offered first.
    best_branches.sort(key=lambda x: x[1], reverse=True)

    return [branch_tuple[0] for branch_tuple in best_branches] # Return only branch indexes


def find_solution_dfs_with_heuristics(self):
    """Use DFS to find a solution path using branch heuristics."""
    print(f"\n=== Finding solution with Heuristic DFS ===")
    if self.solution_path:
        print("Using existing solution path")
        return self.solution_path

    # Create a starting state
    start_branches = self.clone_branches()
    start_state = GameState(start_branches)

    print("Initial state for DFS:")
    start_state.print_state()

    # Setup for DFS
    stack = [(start_state, deque())]  # (state, move_path, depth)
    visited = set([hash(start_state)])  # Use hash to track visited states

    old_path = []
    old_path_size = sys.maxsize

    states_checked = 0

    while stack:
        states_checked += 1
        if states_checked % 100 == 0:
            print(f"DFS progress: {states_checked} states checked, stack size: {len(stack)}")

        current_state, current_path = stack.pop()

        # Check if this is a winning state
        if self.is_game_won(current_state.branches):
            print(f"Solution found! Path length: {len(current_path)}")
            
            if len(current_path) < old_path_size:
                print(f"Found new path with {len(current_path)} moves (previous: {old_path_size})")
                old_path = current_path
                old_path_size = len(current_path)
            continue

        # Get the best branches to start from using our heuristic.
        best_start_branch_idxs = find_best_start_branches(current_state)
        best_ending_branch_idxs = find_best_ending_branches(current_state)

        # TODO: remove
        print("Best starting branches are: ", best_start_branch_idxs, " while best ending branches are ", best_ending_branch_idxs)
        
        # Try all possible moves (prioritizing the best branch first)
        for from_idx in best_start_branch_idxs:
            for to_idx in best_ending_branch_idxs:
                if from_idx == to_idx:
                    continue

                from_branch = current_state.branches[from_idx]
                to_branch = current_state.branches[to_idx]

                if self.is_valid_move(from_branch, to_branch):
                    # Create a new state by cloning the current one
                    new_branches = self.clone_branches(current_state.branches)

                    # Apply the move
                    success = self.apply_move(new_branches, from_idx, to_idx)
                    if success:
                        new_state = GameState(new_branches)
                        new_path = current_path + deque([(from_idx, to_idx)])

                        # Check if we've seen this state before
                        new_state_hash = hash(new_state)
                        if new_state_hash not in visited:
                            visited.add(new_state_hash)
                            stack.append((new_state, new_path))
    
    if old_path:
        print(f"Best solution has {len(old_path)} moves")
    else:
        print(f"No solution found")
    return old_path


def find_solution_dfs(self):
    """Use DFS to find the shortest solution path."""
    if self.solution_path:
        return self.solution_path
    
    start_branches = self.clone_branches()
    start_state = GameState(start_branches)

    # Setup for DFS
    # (state, move_path)
    stack = [(start_state, deque())]
    
    # {state: lengthOfPathToReachState}
    visited = {hash(start_state): 0}

    best_path = None
    best_path_length = sys.maxsize

    while stack:
        current_state, current_path = stack.pop()

        # Check if this is a winning state
        if self.is_game_won(current_state.branches):
            if len(current_path) < best_path_length:
                print("Found new path, old was", best_path_length, "and new is", len(current_path))
                best_path = current_path
                best_path_length = len(current_path)
            continue # Continue to search

        # Try all possible moves
        for from_idx in range(len(current_state.branches)):
            for to_idx in range(len(current_state.branches)):
                if from_idx == to_idx:
                    continue

                from_branch = current_state.branches[from_idx]
                to_branch = current_state.branches[to_idx]

                if self.is_valid_move(from_branch, to_branch):

                    # Clone current state and apply the move
                    new_branches = self.clone_branches(current_state.branches)
                    success = self.apply_move(new_branches, from_idx, to_idx)
                    if success:

                        new_state = GameState(new_branches)
                        new_path = current_path + deque([(from_idx, to_idx)])

                        new_state_hash = hash(new_state)
                        
                        # Check if we've seen this state before
                        # But also check if this path that led to the same state has a shorter way than before.
                        # No negative weights so this is valid...
                        if new_state_hash not in visited or len(new_path) < visited[new_state_hash]:
                            visited[new_state_hash] = len(new_path)
                            stack.append((new_state, new_path))

    if best_path:
        print(f"Best solution has {len(best_path)} moves")
    else:
        print("No solution found")
    return best_path
