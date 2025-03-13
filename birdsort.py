import pygame 
import sys
import random
from algorithms.algorithm_picker import Algorithm, Solver
from state_manager import State
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

from algorithms.dfs import *
from states.gameState import GameState


class Game(State):
    def __init__(self):
        super().__init__()
        self.branches = []
        self.selected_branch = None
        self.setup_level()
        self.moves = 0
        self.completed_branches = 0
        self.font = pygame.font.SysFont(None, 36)
        
        # Create hint buttons
        self.hint_buttons = []
        button_width = 150
        button_height = 50

        algorithms = [["bfs",Algorithm.BFS], ["dfs",Algorithm.DFS], ["dls",Algorithm.DLS], ["astar",Algorithm.ASTAR], ["greedy",Algorithm.GREEDY]]
        total_buttons = len(algorithms)  # Number of algorithms
        total_width = total_buttons * button_width
        spacing = (SCREEN_WIDTH - total_width) // (total_buttons + 1)
        
        for i, algorithm in enumerate(algorithms):
            x = spacing + i * (button_width + spacing)
            y = SCREEN_HEIGHT - button_height - 20
            button = Button(x, y, button_width, button_height, f"Hint ({algorithm[0]})",(200, 200, 255), (150, 150, 255))
            self.hint_buttons.append((button, algorithm))
            
            """
            # Create hint button
            self.hint_button = Button(SCREEN_WIDTH - 200, 20, 180, 50, "Get Hint", 
                                    (200, 200, 255), (150, 150, 255))
            self.hint_from = None
            self.hint_to = None
            self.solution_path = None
        """
        self.hint_from = None
        self.hint_to = None
        self.solution_path = None
        
        # Initialize the game state
        self.game_state = GameState(self.branches)
        
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if any hint button was clicked
            for button, algorithm in self.hint_buttons:
                if button.is_clicked(mouse_pos):
                    print(f"Hint button for {algorithm[0]} clicked")
                    self.get_hint(algorithm[1])
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
                success = self.game_state.apply_move(from_idx,clicked_index)
                
                # success = self.try_move_birds(self.selected_branch, clicked_branch)
                if success:
                    print("Move successful")
                    # Add the move to the game state history
                    self.game_state.move_history.append((from_idx, clicked_index))
                    # Update the game state with current branches
                    self.game_state = GameState(self.branches, self.game_state.move_history)
                    self.moves += 1
                else:
                    print("Move failed")
            self.selected_branch = None

    def print_move(self, from_idx, to_idx):
        from_branch = self.branches[from_idx]

        if from_branch.birds:
            top_color = from_branch.birds[-1].color
            print(f"Move: Branch {from_idx} -> Branch {to_idx} (Color: {top_color})")
        else:
            print(f"Invalid Move: Branch {from_idx} is empty")

    def get_hint(self, algorithm):
        solver = Solver(algorithm)  # TODO: make this be changeable, not hardcoded 

        if not(self.solution_path == self.game_state.move_history):  # TODO: change how caching is being done!
            # Use the game state for the solver
            self.solution_path = solver.find_solution(GameState(self.branches))
        else:  # TODO: remove else, only for debug
            print("Now using cached solution")

        if self.solution_path and len(self.solution_path) > 0:
            print(self.solution_path)
            from_idx, to_idx = self.solution_path[0]
            print(f"Hint suggests moving from branch {from_idx} to {to_idx}")
            self.hint_from = self.branches[from_idx]
            self.hint_to = self.branches[to_idx]
        else:
            print("No hint available - couldn't find solution")
    
    def is_game_over(self):  # TODO: add a state for stalemate
        if(self.game_state.is_solved()):
            return 1
        else:
            return 0


    def update(self):
        pass
    
    def draw(self, surface):
        surface.fill((135, 206, 235))  # Sky blue background
        
        for branch in self.branches:  # TODO: make this use the updated textures
            branch.draw(surface)
        
        # Highlight selected branch
        if self.selected_branch:
            pygame.draw.rect(surface, (255, 255, 255), self.selected_branch.rect, 3)
        
        # Highlight hint branches
        if self.hint_from:
            pygame.draw.rect(surface, (0, 255, 0), self.hint_from.rect, 3)  # Green for source
        if self.hint_to:
            pygame.draw.rect(surface, (255, 165, 0), self.hint_to.rect, 3)  # Orange for target
        
        # Draw hint buttons
        for button, _ in self.hint_buttons:
            button.draw(surface)
        
        # Draw UI
        moves_text = self.font.render(f"Moves: {self.moves}", True, (0, 0, 0))
        surface.blit(moves_text, (20, 20))
        
        completed_text = self.font.render(f"Completed: {self.completed_branches}/{len(COLORS)}", True, (0, 0, 0))
        surface.blit(completed_text, (20, 60))
        
        # Instructions
        help_text = self.font.render("Click to select a branch, then click another to move birds", True, (0, 0, 0))
        surface.blit(help_text, (SCREEN_WIDTH//2 - 240, 20))
        
        # Check if player won
        if (self.is_game_over() == 1):
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
    
    def get_game_state(self):
        """Return the current game state."""
        return self.game_state