import sys
from collections import deque
import time

def find_solution(self, first_accept=True):
    """Use DFS to find the shortest solution path."""
    start_time = time.time()

    start_state = self.clone()

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
        if current_state.is_solved():
            if first_accept:
                best_path = current_path
                break
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

                #if self.is_valid_move(from_branch, to_branch):

                # Clone current state and apply the move
                new_state = current_state.clone()
                success = new_state.apply_move(from_idx, to_idx)
                if success:

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

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.5f} seconds")
    return best_path


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

