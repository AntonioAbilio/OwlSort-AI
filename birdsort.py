import pygame
import sys
import random
import copy
from collections import deque

from models.bird import Bird
from models.branch import Branch
from models.button import Button
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BRANCH_WIDTH,
    BRANCH_HEIGHT,
    MAX_BIRDS_PER_BRANCH,
    COLORS
)

# Initialize pygame
pygame.init()



# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bird Sort 2: Color Puzzle")
clock = pygame.time.Clock()


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

class Game:
    def __init__(self):
        self.branches = []
        self.selected_branch = None
        self.setup_level()
        self.moves = 0
        self.completed_branches = 0
        self.font = pygame.font.SysFont(None, 36)
        
        # Create hint button
        self.hint_button = Button(SCREEN_WIDTH - 200, 20, 180, 50, "Get Hint", 
                                 (200, 200, 255), (150, 150, 255))
        self.hint_from = None
        self.hint_to = None
        self.solution_path = None
        
    def setup_level(self):
        # Create branches with zigzag layout (left to right, top to bottom)
        branch_count = 6  # 4 for birds + 2 empty for sorting
        margin = 100
        rows = 3
        cols = 2
        id = 0
        
        for row in range(rows):
            for col in range(cols):
                # Alternate between left and right sides
                if col == 0:  # Left side
                    x = margin
                else:  # Right side
                    x = SCREEN_WIDTH - margin - BRANCH_WIDTH
                
                y = margin + row * (BRANCH_HEIGHT + 100)
                self.branches.append(Branch(x, y, id))
                id += 1
        
        # Generate a solvable distribution of birds
        all_birds = []
        
        # Create exactly MAX_BIRDS_PER_BRANCH birds of each color
        for color in COLORS:
            for _ in range(MAX_BIRDS_PER_BRANCH):
                all_birds.append(Bird(color))
        
        # Shuffle all birds
        random.shuffle(all_birds)
        
        # Distribute birds across the first 4 branches
        bird_index = 0
        for i in range(4):  # Fill the first 4 branches
            branch = self.branches[i]
            for j in range(MAX_BIRDS_PER_BRANCH):
                if bird_index < len(all_birds):
                    branch.add_bird(all_birds[bird_index])
                    bird_index += 1
        
        print("Initial game setup complete")
        self.print_game_state()
    
    def print_game_state(self):
        """Print the current game state for debugging"""
        print("\nCurrent Game State:")
        for i, branch in enumerate(self.branches):
            birds_colors = [f"{bird.color}" for bird in branch.birds]
            print(f"  Branch {i}: {birds_colors}")
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if hint button was clicked
            if self.hint_button.is_clicked(mouse_pos):
                print("Hint button clicked")
                self.get_hint()
                return
            
            self.handle_click(mouse_pos)
    
    def handle_click(self, pos):
        clicked_branch = None
        
        # Check if any branch was clicked
        for i, branch in enumerate(self.branches):
            if branch.rect.collidepoint(pos) and not branch.is_completed:
                clicked_branch = branch
                clicked_index = i
                print(f"Branch {i} clicked")
                break
        
        if clicked_branch is None:
            return
        
        # Clear any hint highlights
        self.hint_from = None
        self.hint_to = None
        
        # If no branch is currently selected, select this one if it has birds
        if self.selected_branch is None:
            if clicked_branch.birds:
                self.selected_branch = clicked_branch
                print(f"Selected branch with {len(clicked_branch.birds)} birds")
        else:
            # Attempting to move birds from selected branch to clicked branch
            if self.selected_branch != clicked_branch:
                # Find indices for logging
                for i, branch in enumerate(self.branches):
                    if branch == self.selected_branch:
                        from_idx = i
                
                print(f"Attempting to move birds from branch {from_idx} to branch {clicked_index}")
                success = self.try_move_birds(self.selected_branch, clicked_branch)
                if success:
                    print("Move successful")
                    self.print_game_state()
                else:
                    print("Move failed")
            self.selected_branch = None
    
    def try_move_birds(self, from_branch, to_branch):
        # Check if move is valid
        if not from_branch.birds or to_branch.is_completed:
            print("Invalid move: source branch empty or target branch completed")
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
        
        print(f"Attempting to move {len(birds_to_move)} birds of color {top_bird_color}")
        
        # Check if target branch can accept these birds
        if not to_branch.birds:
            # Empty branch can accept any birds if there's space
            can_move = len(birds_to_move) <= MAX_BIRDS_PER_BRANCH - len(to_branch.birds)
            print(f"Target branch is empty, can move: {can_move}")
        else:
            # Non-empty branch can only accept matching color birds if there's space
            can_move = (to_branch.birds[-1].color == top_bird_color and 
                         len(birds_to_move) <= MAX_BIRDS_PER_BRANCH - len(to_branch.birds))
            print(f"Target branch has color {to_branch.birds[-1].color}, can move: {can_move}")
        
        if can_move:
            # Remove birds from source branch (in reverse to maintain order)
            for _ in range(len(birds_to_move)):
                from_branch.birds.pop()
            
            # Add birds to target branch
            for bird in birds_to_move:
                to_branch.add_bird(bird)
            
            self.moves += 1
            print(f"Move completed. Total moves: {self.moves}")
            
            # Check if the target branch is now complete
            if to_branch.check_completion():
                self.completed_branches += 1
                print(f"Branch completed! Total completed: {self.completed_branches}")
                
            # Check if the user has actually used the hint.
            if self.solution_path:
                oldState = (self.branches.index(from_branch), self.branches.index(to_branch))
                if self.solution_path[0] == oldState:
                    self.solution_path.popleft()
                else:
                    self.solution_path = None

            return True
        
        return False
    
    def is_valid_move(self, from_branch, to_branch):
        """Check if a move from one branch to another is valid without actually moving birds."""
        if not from_branch.birds or to_branch.is_completed:
            return False
        
        top_bird_color = from_branch.birds[-1].color
        
        # Count birds of same color at top
        birds_to_move_count = 0
        for i in range(len(from_branch.birds) - 1, -1, -1):
            if from_branch.birds[i].color == top_bird_color:
                birds_to_move_count += 1
            else:
                break
        
        if not to_branch.birds:
            # Empty branch can accept any birds if there's space
            return birds_to_move_count <= MAX_BIRDS_PER_BRANCH
        else:
            # Non-empty branch needs matching color and sufficient space
            return (to_branch.birds[-1].color == top_bird_color and 
                   birds_to_move_count <= MAX_BIRDS_PER_BRANCH - len(to_branch.birds))
    
    def is_game_won(self, branches=None):
        """Check if game is won (all color groups completed)."""
        if branches is None:
            branches = self.branches
            
        completed_count = 0
        for branch in branches:
            if len(branch.birds) == MAX_BIRDS_PER_BRANCH:
                if all(bird.color == branch.birds[0].color for bird in branch.birds):
                    completed_count += 1
        
        return completed_count == len(COLORS)
    
    def clone_branches(self, source_branches=None):
        """Create a deep copy of the branches for BFS."""
        if source_branches is None:
            source_branches = self.branches
            
        new_branches = []
        for branch in source_branches:
            new_branch = Branch(branch.x, branch.y, branch.id)
            new_branch.side = branch.side
            new_branch.is_completed = branch.is_completed
            # Copy birds
            for bird in branch.birds:
                new_bird = Bird(bird.color)
                new_branch.birds.append(new_bird)
            new_branches.append(new_branch)
        return new_branches
    
    def apply_move(self, branches, from_idx, to_idx):
        """Apply a move to a copied set of branches."""
        from_branch = branches[from_idx]
        to_branch = branches[to_idx]
        
        if not from_branch.birds:
            return False
        
        top_bird_color = from_branch.birds[-1].color
        
        # Find birds to move
        birds_to_move = []
        for i in range(len(from_branch.birds) - 1, -1, -1):
            if from_branch.birds[i].color == top_bird_color:
                birds_to_move.insert(0, from_branch.birds[i])
            else:
                break
        
        # Check if we can move
        if not to_branch.birds:
            can_move = len(birds_to_move) <= MAX_BIRDS_PER_BRANCH - len(to_branch.birds)
        else:
            can_move = (to_branch.birds[-1].color == top_bird_color and 
                       len(birds_to_move) <= MAX_BIRDS_PER_BRANCH - len(to_branch.birds))
        
        if can_move:
            # Move the birds
            for _ in range(len(birds_to_move)):
                from_branch.birds.pop()
            
            for bird in birds_to_move:
                to_branch.add_bird(bird)
                
            # Check completion
            if len(to_branch.birds) == MAX_BIRDS_PER_BRANCH:
                if all(bird.color == to_branch.birds[0].color for bird in to_branch.birds):
                    to_branch.is_completed = True
            
            return True
            
        return False
    
    def print_move(self, from_idx, to_idx):
        """Print a move for debugging"""
        from_branch = self.branches[from_idx]
        to_branch = self.branches[to_idx]
        if from_branch.birds:
            top_color = from_branch.birds[-1].color
            print(f"Move: Branch {from_idx} -> Branch {to_idx} (Color: {top_color})")
        else:
            print(f"Invalid Move: Branch {from_idx} is empty")
    
    def find_solution_bfs(self):
        print("\n=== Finding solution with BFS ===")
        """Use BFS to find the shortest solution path."""
        if self.solution_path:
            print("Using existing solution path")
            return self.solution_path
            
        # Create a starting state
        start_branches = self.clone_branches()
        start_state = GameState(start_branches)
        
        print("Initial state for BFS:")
        start_state.print_state()
        
        # Setup for BFS
        queue = deque([(start_state, deque())])  # (state, move_path)
        visited = set([hash(start_state)])  # Use hash to track visited states
        
        states_checked = 0
        max_queue_size = 1
        
        while queue:
            states_checked += 1
            if states_checked % 100 == 0:
                print(f"BFS progress: {states_checked} states checked, queue size: {len(queue)}")
            
            max_queue_size = max(max_queue_size, len(queue))
            current_state, current_path = queue.popleft()
            
            # Check if this is a winning state
            if self.is_game_won(current_state.branches):
                print(f"Solution found! Path length: {len(current_path)}")
                print(f"BFS stats: {states_checked} states checked, max queue size: {max_queue_size}")
                self.solution_path = current_path
                return current_path
            
            # Try all possible moves
            for from_idx in range(len(current_state.branches)):
                for to_idx in range(len(current_state.branches)):
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
                                queue.append((new_state, new_path))
        
        print("No solution found after checking", states_checked, "states")
        return None
    
    def get_hint(self):
        """Get a hint for the next move."""
        print("Getting hint...")

        # Check if the last move was made using the hint
        # If so then use the list of the saved solutions

        if not(self.solution_path):
            self.solution_path = self.find_solution_bfs()
        else: # TODO: remove else, only for debug
            print("Now using cached solution")

        if self.solution_path and len(self.solution_path) > 0:
            # Get the next move from the solution
            print(self.solution_path)
            from_idx, to_idx = self.solution_path[0]
            print(f"Hint suggests moving from branch {from_idx} to {to_idx}")
            self.hint_from = self.branches[from_idx]
            self.hint_to = self.branches[to_idx]
        else:
            print("No hint available - couldn't find solution")
    
    def update(self):
        pass
    
    def draw(self, surface):
        # Clear screen
        surface.fill((135, 206, 235))  # Sky blue background
        
        # Draw all branches
        for branch in self.branches:
            branch.draw(surface)
        
        # Highlight selected branch
        if self.selected_branch:
            pygame.draw.rect(surface, (255, 255, 255), self.selected_branch.rect, 3)
        
        # Highlight hint branches
        if self.hint_from:
            pygame.draw.rect(surface, (0, 255, 0), self.hint_from.rect, 3)  # Green for source
        if self.hint_to:
            pygame.draw.rect(surface, (255, 165, 0), self.hint_to.rect, 3)  # Orange for target
        
        # Draw hint button
        self.hint_button.draw(surface)
        
        # Draw UI
        moves_text = self.font.render(f"Moves: {self.moves}", True, (0, 0, 0))
        surface.blit(moves_text, (20, 20))
        
        completed_text = self.font.render(f"Completed: {self.completed_branches}/{len(COLORS)}", True, (0, 0, 0))
        surface.blit(completed_text, (20, 60))
        
        # Instructions
        help_text = self.font.render("Click to select a branch, then click another to move birds", True, (0, 0, 0))
        surface.blit(help_text, (SCREEN_WIDTH//2 - 240, 20))
        
        # Check if player won
        if self.completed_branches == len(COLORS):
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
            
            # Draw win message
            win_font = pygame.font.SysFont(None, 72)
            win_text = win_font.render("You Won!", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            surface.blit(win_text, win_rect)
            
            moves_result = self.font.render(f"Total Moves: {self.moves}", True, (255, 255, 255))
            moves_rect = moves_result.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            surface.blit(moves_result, moves_rect)

def main():
    game = Game()
    print("Game initialized. Press the hint button to test BFS algorithm.")
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    