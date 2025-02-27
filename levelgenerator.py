import random
import time
import xml.etree.ElementTree as ET
from collections import deque
import argparse

# Game constants (conceptual, no longer tied to pygame)
SCREEN_WIDTH = 1280  # Just used for conceptual positioning, not actual rendering
SCREEN_HEIGHT = 720  # Just used for conceptual positioning, not actual rendering
BRANCH_WIDTH = 200   # Conceptual width
BRANCH_HEIGHT = 60   # Conceptual height
MAX_BIRDS_PER_BRANCH = 5
COLORS = [
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
]

class Bird:
    def __init__(self, color):
        self.color = color
        
    def __eq__(self, other):
        if not isinstance(other, Bird):
            return False
        return self.color == other.color
    
    def __hash__(self):
        return hash(self.color)

class Branch:
    def __init__(self, x, y):
        if x < (SCREEN_WIDTH/2): self.side = "left"
        else: self.side = "right"
        self.x = x
        self.y = y
        self.birds = []
        self.rect = {"x": x, "y": y, "width": BRANCH_WIDTH, "height": BRANCH_HEIGHT}  # Replace pygame.Rect
        self.is_completed = False
    
    def add_bird(self, bird):
        if len(self.birds) < MAX_BIRDS_PER_BRANCH and not self.is_completed:
            self.birds.append(bird)
            return True
        return False
    
    def check_completion(self):
        # Branch is complete if it has birds and all are the same color
        if not self.birds:
            return False
            
        first_color = self.birds[0].color
        if len(self.birds) == MAX_BIRDS_PER_BRANCH and all(bird.color == first_color for bird in self.birds):
            self.is_completed = True
            return True
        return False
    
    def __eq__(self, other):
        if not isinstance(other, Branch):
            return False
        if len(self.birds) != len(other.birds):
            return False
        for i in range(len(self.birds)):
            if self.birds[i].color != other.birds[i].color:
                return False
        return True

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

class LevelGenerator:
    def __init__(self, num_branches=6):
        self.num_branches = num_branches
        self.BRANCH_POSITIONS = self.calculate_branch_positions()
    
    def calculate_branch_positions(self):
        """Calculate virtual positions for branches - can handle any number without visual constraints"""
        positions = []
        
        # Calculate the number of virtual rows and columns needed
        # This is just for conceptual positioning in the XML, not for actual rendering
        virtual_rows = (self.num_branches + 1) // 2
        
        for i in range(self.num_branches):
            # Determine if this is a left or right branch (alternating)
            is_left = i % 2 == 0
            
            # Calculate row based on position
            virtual_row = i // 2
            
            # Set virtual x position
            if is_left:
                x = 100  # Left margin
            else:
                x = SCREEN_WIDTH - 100 - BRANCH_WIDTH  # Right side
            
            # Set virtual y position
            y = 100 + (virtual_row * 100)
            
            # For branches that would exceed the virtual screen height,
            # we'll wrap them and use additional columns
            if y + BRANCH_HEIGHT > SCREEN_HEIGHT:
                # Calculate how many branches we can fit in a column
                branches_per_col = SCREEN_HEIGHT // 100
                
                # Determine which overflow column we're in
                overflow_col = virtual_row // branches_per_col
                
                # Adjust y to wrap within height
                y = 100 + (virtual_row % branches_per_col) * 100
                
                # Shift x based on overflow column (creating additional columns)
                if is_left:
                    x = 100 + (overflow_col * 250)
                else:
                    x = SCREEN_WIDTH - 100 - BRANCH_WIDTH - (overflow_col * 250)
            
            positions.append((x, y))
        
        return positions
    
    def generate_level(self):
        """Generate a random level setup"""
        branches = []
        
        # Create branches with positions
        for x, y in self.BRANCH_POSITIONS:
            branches.append(Branch(x, y))
        
        # Generate a distribution of birds
        all_birds = []
        
        # Create exactly MAX_BIRDS_PER_BRANCH birds of each color
        for color in COLORS:
            for _ in range(MAX_BIRDS_PER_BRANCH):
                all_birds.append(Bird(color))
        
        # Shuffle all birds
        random.shuffle(all_birds)
        
        # Distribute birds across the first num_branches - 2 branches
        bird_index = 0
        for i in range(min(self.num_branches - 2, len(branches))):  # Fill all but last 2 branches
            branch = branches[i]
            for j in range(MAX_BIRDS_PER_BRANCH):
                if bird_index < len(all_birds):
                    branch.add_bird(all_birds[bird_index])
                    bird_index += 1
        
        return branches
    
    def clone_branches(self, source_branches):
        """Create a deep copy of the branches for BFS."""
        new_branches = []
        for branch in source_branches:
            new_branch = Branch(branch.x, branch.y)
            new_branch.side = branch.side
            new_branch.is_completed = branch.is_completed
            # Copy birds
            for bird in branch.birds:
                new_bird = Bird(bird.color)
                new_branch.birds.append(new_bird)
            new_branches.append(new_branch)
        return new_branches
    
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
    
    def is_game_won(self, branches):
        """Check if game is won (all color groups completed)."""
        completed_count = 0
        for branch in branches:
            if len(branch.birds) == MAX_BIRDS_PER_BRANCH:
                if all(bird.color == branch.birds[0].color for bird in branch.birds):
                    completed_count += 1
        
        return completed_count == len(COLORS)
    
    def measure_difficulty(self, branches):
        """Measure difficulty based on BFS performance with timeout"""
        # Create a starting state
        start_state = GameState(branches)
        
        # Setup for BFS
        queue = deque([(start_state, [])])  # (state, move_path)
        visited = set([hash(start_state)])  # Use hash to track visited states
        
        states_checked = 0
        max_queue_size = 1
        solution_path = None
        start_time = time.time()
        timeout = 20.0  # Timeout in seconds
        
        while queue:
            # Check for timeout
            if time.time() - start_time > timeout:
                print("BFS search timed out - considering level unsolvable")
                break
                
            states_checked += 1
            
            # Limit the maximum states to check to prevent excessive CPU usage
            if states_checked > 100000:  # Add a reasonable limit
                print("Exceeded maximum states - considering level unsolvable")
                break

            current_state, current_path = queue.popleft()
            
            # Check if this is a winning state
            if self.is_game_won(current_state.branches):
                solution_path = current_path
                break
            
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
                            new_path = current_path + [(from_idx, to_idx)]
                            
                            # Check if we've seen this state before
                            new_state_hash = hash(new_state)
                            if new_state_hash not in visited:
                                visited.add(new_state_hash)
                                queue.append((new_state, new_path))
        
        solve_time = time.time() - start_time
        
        # Return metrics for difficulty calculation
        return {
            'solution_found': solution_path is not None,
            'solution_length': len(solution_path) if solution_path else float('inf'),
            'states_checked': states_checked,
            'max_queue_size': max_queue_size,
            'solve_time': solve_time,
        }
    
    def generate_levels(self, count):
        """Generate and rate multiple levels"""
        levels = []
        total_attempts = 0
        max_attempts_per_level = 20
        max_total_attempts = count * 50  # Overall safety limit
        
        print(f"Generating {count} levels and rating their difficulty...")
        i = 0
        while i < count and total_attempts < max_total_attempts:
            total_attempts += 1
            attempts_for_current = 0
            
            if i % 5 == 0 or i == count - 1:
                print(f"Working on level {i+1}/{count}... (total attempts: {total_attempts})")
            
            # Generate a level
            branches = self.generate_level()
            
            # Make a deep copy before analysis
            branches_copy = self.clone_branches(branches)
            
            # Measure difficulty
            difficulty_metrics = self.measure_difficulty(branches_copy)
            
            # Skip unsolvable levels, but with limits
            if not difficulty_metrics['solution_found']:
                attempts_for_current += 1
                if attempts_for_current >= max_attempts_per_level:
                    print(f"Warning: Moving to next level after {attempts_for_current} failed attempts")
                    i += 1  # Move on to next level even if we can't solve this one
                continue
            
            # Save level data and its difficulty
            levels.append({
                'branches': branches,
                'difficulty': difficulty_metrics,
                'difficulty_score': self.calculate_difficulty_score(difficulty_metrics)
            })
            i += 1
        
        # Sort levels by difficulty
        levels.sort(key=lambda x: x['difficulty_score'])
        
        if total_attempts >= max_total_attempts:
            print(f"Warning: Reached maximum generation attempts ({max_total_attempts})")
        
        return levels 
    
    def calculate_difficulty_score(self, metrics):
        """Calculate a single difficulty score from the metrics"""
        if not metrics['solution_found']:
            return float('inf')  # Unsolvable levels get infinite difficulty
        
        # Combine metrics into a single score
        # States checked is the primary factor, but solution length and queue size also matter
        score = (
            metrics['states_checked'] * 1.0 + 
            metrics['solution_length'] * 10.0 + 
            metrics['max_queue_size'] * 0.5 +
            metrics['solve_time'] * 100.0
        )
        
        return score
    
    def save_levels_to_xml(self, levels, filename="bird_sort_levels.xml"):
        """Save generated levels to an XML file"""
        root = ET.Element('levels')
        
        for i, level_data in enumerate(levels):
            level_elem = ET.SubElement(root, 'level')
            level_elem.set('id', str(i+1))
            level_elem.set('difficulty_score', str(round(level_data['difficulty_score'], 2)))
            
            # Add difficulty metrics
            metrics = level_data['difficulty']
            metrics_elem = ET.SubElement(level_elem, 'metrics')
            metrics_elem.set('states_checked', str(metrics['states_checked']))
            metrics_elem.set('solution_length', str(metrics['solution_length']))
            metrics_elem.set('max_queue_size', str(metrics['max_queue_size']))
            metrics_elem.set('solve_time', str(round(metrics['solve_time'], 3)))
            
            # Add branch data
            branches_elem = ET.SubElement(level_elem, 'branches')
            for j, branch in enumerate(level_data['branches']):
                branch_elem = ET.SubElement(branches_elem, 'branch')
                branch_elem.set('id', str(j))
                branch_elem.set('x', str(branch.x))
                branch_elem.set('y', str(branch.y))
                
                for k, bird in enumerate(branch.birds):
                    bird_elem = ET.SubElement(branch_elem, 'bird')
                    bird_elem.set('index', str(k))
                    # Store color as a tuple string
                    color_str = str(bird.color)
                    bird_elem.set('color', color_str)
        
        # Create XML tree and save to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Saved {len(levels)} levels to {filename}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate levels for Bird Sort game')
    parser.add_argument('count', type=int, help='Number of levels to generate')
    parser.add_argument('--output', '-o', default='bird_sort_levels.xml', help='Output XML file name')
    parser.add_argument('--branches', '-b', type=int, default=6, help='Number of branches per level')
    
    args = parser.parse_args()
    
    if args.count < 1:
        print("Error: Number of levels must be at least 1")
        return
    
    if args.branches < len(COLORS) + 2:
        print(f"Error: Number of branches must be at least {len(COLORS) + 2} (colors + 2 empty branches)")
        return
    
    generator = LevelGenerator(num_branches=args.branches)
    levels = generator.generate_levels(args.count)
    generator.save_levels_to_xml(levels, args.output)
    
    # Print difficulty summary
    print("\nDifficulty Summary:")
    for i, level in enumerate(levels):
        metrics = level['difficulty']
        print(f"Level {i+1}: Score={round(level['difficulty_score'], 2)}, " +
              f"Steps={metrics['solution_length']}, States={metrics['states_checked']}")

if __name__ == "__main__":
    main()