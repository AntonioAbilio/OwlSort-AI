import pygame 
import sys
import random
import math
from algorithms.algorithm_picker import Algorithm, Solver
from windows.state_manager import State
from collections import deque
from algorithms.solution_cache import SolutionCache


from models.bird import Bird
from models.branch import Branch
from models.button import Button

import constants

from algorithms.dfs import *
from states.gameState import GameState


class Game(State):
    def __init__(self, num_branches, bird_list=[], num_colors=4, is_custom=False):
        super().__init__()
        self.branches = []
        constants.num_colors = num_colors
        self.selected_branch = None
        self.setup_level(num_branches, bird_list, is_custom)
        self.moves = 0
        self.completed_branches = 0
        self.font = pygame.font.SysFont(None, 36)

        self.solution_cache = SolutionCache()
        self.last_algorithm = None
        
        # Create hint buttons
        self.hint_buttons = []
        button_width = 150
        button_height = 50


        algorithms = [["bfs",Algorithm.BFS], ["dfs-FA",Algorithm.DFS_FIRST_ACCEPT], ["dfs-Best",Algorithm.DFS_BEST], 
                      ["dls",Algorithm.DLS], ["it_deep",Algorithm.IT_DEEP], ["astar",Algorithm.ASTAR], 
                      ["wastar",Algorithm.WASTAR], ["greedy",Algorithm.GREEDY], ["uniform",Algorithm.UNIFORM]]
        
        total_buttons = len(algorithms)
        total_width = total_buttons * button_width
        spacing = (constants.SCREEN_WIDTH - total_width) // (total_buttons + 1)
        
        for i, algorithm in enumerate(algorithms):
            x = spacing + i * (button_width + spacing)
            y = constants.SCREEN_HEIGHT - button_height - 20
            button = Button(x, y, button_width, button_height, f"Hint ({algorithm[0]})",(200, 200, 255), (150, 150, 255))
            self.hint_buttons.append((button, algorithm))
            
        self.hint_from = None
        self.hint_to = None
        self.solution_path = None
        
        # Initialize the game state
        self.game_state = GameState(self.branches)

        self.current_solver = None
        self.loading_dots = 0
        self.loading_timer = 0
        
    def setup_level(self, num_branches, bird_list, is_custom):
        # Create branches with zigzag layout (left to right, top to bottom)
        margin = 0
        upper_offset = 150
        id = 0
        x = 0
        y = 0
        row = 0
        left = True
        all_birds = []
        
        if not is_custom:
            random_birds=[]
            # Create exactly MAX_BIRDS_PER_BRANCH birds of each color
            for color in constants.COLORS:
                for _ in range(constants.MAX_BIRDS_PER_BRANCH):
                    random_birds.append(Bird(color))
            random.shuffle(random_birds) # Shuffle all birds
            bird_index = 0
            for i in range(num_branches):  # FIXME: Make this not hardcoded
                branch = []
                for j in range(constants.MAX_BIRDS_PER_BRANCH):
                    if bird_index < len(random_birds):
                        branch.append(random_birds[bird_index])
                        bird_index += 1
                    else:
                        break
                all_birds.append(branch)
        else:
            all_birds = bird_list
    
        for i, branch_data in enumerate(all_birds):
            y = upper_offset + row * (constants.BRANCH_HEIGHT + 100)
            if left:
                x = margin
            else:
                x = constants.SCREEN_WIDTH - margin - constants.BRANCH_WIDTH
                row += 1
            branch = Branch(x, y, id)
            for color in branch_data:
                branch.add_bird(color)
            self.branches.append(branch)
            left = not left
            id += 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if any hint button was clicked
            for button, algorithm in self.hint_buttons:
                if button.is_clicked(mouse_pos):
                    print(f"Hint button for {algorithm[0]} clicked")
                    self.get_hint(algorithm)
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
                    if self.last_algorithm is not None:
                        self.solution_cache.update_after_move(self.game_state, (from_idx, clicked_index))
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
        if self.current_solver and self.current_solver.is_running:
            if self.current_solver.algorithm != algorithm[1]:
                print("Already solving, please wait...")
                return
            else:
                # Cancel the current solver
                self.current_solver.cancel()
                return
        
        # Check if we already have a cached solution for this state and algorithm
        self.solution_path = self.solution_cache.get_solution(self.game_state, algorithm[1])
        

        if self.solution_path is None:
            self.current_solver = Solver(algorithm[1])
            self.current_solver.algorithm_name = algorithm[0]

            self.current_solver.find_solution(GameState(self.branches, isMock=True), self.solution_callback)
            

        else:
            print(f"Using cached solution")
            # Display the hint
            self.setHint(self.solution_path)
        
        self.last_algorithm = algorithm


    def solution_callback(self, solution, algorithm):
        """Callback for when a solution is found"""
        self.solution_path = solution
        # Cache the solution
        if solution:
            self.solution_cache.store_solution(self.game_state, algorithm, self.solution_path)

        # Display the hint
        self.setHint(solution)
        
        # Reset current_solver after processing
        self.current_solver = None

    def setHint(self, solution):
        if solution:
            from_idx, to_idx = solution[0]
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
        
        # Draw hint buttons (with loading state if active)
        for button, algorithm_info in self.hint_buttons:
            # Check if this button's algorithm is currently running
            is_loading = (self.current_solver and 
                            self.current_solver.algorithm == algorithm_info[1] and
                            self.current_solver.is_running)
            
            if is_loading:
                # Change button color to indicate active state
                original_text = button.text
                dots = "." * self.loading_dots
                button.color = (150, 150, 200)  # Slightly different color
                button.draw(surface)
                button.text = original_text
                button.color = (200, 200, 255)  # Reset to original
                
                # Draw elapsed time
                elapsed = self.current_solver.get_elapsed_time()

                if elapsed > constants.ALGORITHM_TIMEOUT: #TODO: maybe dont do this here?
                    self.current_solver.cancel()
                    print(f"Algorithm {algorithm_info[0]} took too long and was cancelled")

                time_text = self.font.render(f"{elapsed:.1f}s", True, (0, 0, 0))
                time_rect = time_text.get_rect(center=(button.x + button.width//2, 
                                                        button.y - 10))
                surface.blit(time_text, time_rect)
            else:
                button.draw(surface)
        
        # Draw UI
        moves_text = self.font.render(f"Moves: {self.moves}", True, (0, 0, 0))
        surface.blit(moves_text, (20, 20))
        
        completed_text = self.font.render(f"Completed: {self.completed_branches}/{len(constants.COLORS)}", True, (0, 0, 0))
        surface.blit(completed_text, (20, 60))
        
        # Instructions
        help_text = self.font.render("Click to select a branch, then click another to move birds", True, (0, 0, 0))
        surface.blit(help_text, (constants.SCREEN_WIDTH//2 - 240, 20))

        """      
        # If a solver is running, show a more prominent loading indicator
        if self.current_solver and self.current_solver.is_running:
            algo_name = self.current_solver.algorithm_name
            dots = "." * self.loading_dots
            loading_text = self.font.render(f"Running {algo_name}{dots}", True, (0, 0, 0))
            loading_rect = loading_text.get_rect(center=(constants.SCREEN_WIDTH//2, 100))
            surface.blit(loading_text, loading_rect)
            
            # Show elapsed time
            elapsed = self.current_solver.get_elapsed_time()
            time_text = self.font.render(f"Time: {elapsed:.1f}s", True, (0, 0, 0))
            time_rect = time_text.get_rect(center=(constants.SCREEN_WIDTH//2, 130))
            surface.blit(time_text, time_rect)
        """ 
        
        # Check if player won
        if (self.is_game_over() == 1):
            # Draw semi-transparent overlay
            overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
            
            # Draw win message
            win_font = pygame.font.SysFont(None, 72)
            win_text = win_font.render("You Won!", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2))
            surface.blit(win_text, win_rect)
            
            moves_result = self.font.render(f"Total Moves: {self.moves}", True, (255, 255, 255))
            moves_rect = moves_result.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2 + 60))
            surface.blit(moves_result, moves_rect)
        
    def get_game_state(self):
        """Return the current game state."""
        return self.game_state

    def check_level_possible(self):
        solver = Solver(Algorithm.ASTAR) 
        if (solver.find_solution(GameState(self.branches)) != []):
            return True
        return False
    