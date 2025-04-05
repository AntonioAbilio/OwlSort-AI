import random
from global_vars import Globals
from collections import Counter
import ast
from models.bird import Bird
from models.branch import Branch

class LevelGenerator:
    def generate_level(self, num_branches=6, max_birds_per_branch=4, num_colors=4, bird_list=None):
        # Create branches with zigzag layout (left to right, top to bottom)
        all_birds = []
        branches = []
        
        Globals.MAX_BIRDS_PER_BRANCH = max_birds_per_branch
        Globals.TOTAL_BIRDS_PER_COLOR = max_birds_per_branch 
        
        if bird_list == None: # Generate random birds (level is not custom)
            random_birds=[]
            # Create exactly MAX_BIRDS_PER_BRANCH birds of each color
            for color in Globals.COLORS:
                for _ in range(max_birds_per_branch):
                    random_birds.append(Bird(color))
            random.shuffle(random_birds) # Shuffle all birds
            bird_index = 0
            for _ in range(num_branches):
                branch = []
                for j in range(max_birds_per_branch):
                    if bird_index < len(random_birds):
                        branch.append(random_birds[bird_index])
                        bird_index += 1
                    else:
                        break
                all_birds.append(branch)
        else: # Level is custom
            all_birds = bird_list

        self.create_game_structure(all_birds)
        return branches
    
    def generate_level_from_file(self, file_path):
        with open(file_path, 'r') as file:
            # Remove comments and empty lines
            lines = []
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Remove inline comments (after #)
                line = line.split('#')[0].strip()
                if line:
                    lines.append(line)
            content = " ".join(lines)
            
            # Convert the string representation into list of lists
            try:
                rgb_list = ast.literal_eval(content)
                branches = self.parse_level(rgb_list)
                (color_counts, max_birds_per_branch, total_birds_per_color) = self.validate_birds(rgb_list)
                Globals.MAX_BIRDS_PER_BRANCH = max_birds_per_branch
                Globals.TOTAL_BIRDS_PER_COLOR = total_birds_per_color                
                if color_counts is None:
                    print("Invalid level: Number of birds per color is not balanced.")
                    return None
                elif (total_birds_per_color > 7) or (max_birds_per_branch > 7):
                    print("Invalid level: Too many birds per color.")
                    return None
                elif max_birds_per_branch < total_birds_per_color:
                    print("Invalid level: Branches are not big enough.")
                    return None
                elif len(branches) > 10:
                    print("Invalid level: Too many branches.")
                    return None
                else: # Level is valid
                    level = self.create_game_structure(branches)
                    return (level, color_counts, max_birds_per_branch)
            except (SyntaxError, ValueError) as e:
                print(f"Error parsing file: {e}")
                return None  
        
    def create_game_structure(self, all_birds):
        branches = []
        margin = 50
        upper_offset = 150
        id = 0
        x = 0
        y = 0
        row = 0
        left = True
        
        for _, branch_data in enumerate(all_birds):
            y = upper_offset + row * (Globals.BRANCH_HEIGHT + 100)
            if left:
                x = 0 - Globals.BRANCH_WIDTH + Globals.MAX_BIRDS_PER_BRANCH*(Globals.BIRD_SIZE+20) + margin
            else:
                x = Globals.SCREEN_WIDTH - Globals.MAX_BIRDS_PER_BRANCH*(Globals.BIRD_SIZE+20) - margin
                row += 1
            branch = Branch(x, y, id)
            for color in branch_data:
                branch.add_bird(color)
            branches.append(branch)
            left = not left
            id += 1
        return branches        
    
    def parse_level(self, level_data) :
        branches = []
        for branch_data in level_data:
            branch = []
            for bird_color in branch_data:
                bird = Bird(bird_color)
                branch.append(bird)
            branches.append(branch)
        return branches
    
    def validate_birds(self, rgb_list):
        flat_list = [color for row in rgb_list for color in row]  # Flatten the nested list
        color_counts = Counter(flat_list)

        # Check if all colors have exactly x occurrences
        valid = all(count == list(color_counts.values())[0] for count in color_counts.values())
        
        max_branch_size = 0
        for branch in rgb_list:
            if len(branch) > max_branch_size:
                max_branch_size = len(branch)
        
        if valid:
            total_birds_per_color = list(color_counts.values())[0]
            if total_birds_per_color > max_branch_size:
                max_branch_size = total_birds_per_color
            return len(color_counts), max_branch_size, total_birds_per_color
        return None
    