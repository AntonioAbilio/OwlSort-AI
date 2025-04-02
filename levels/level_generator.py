import random
import constants
from models.bird import Bird
from models.branch import Branch

class LevelGenerator:
    def generate_level(num_branches=6, max_birds_per_branch=4, num_colors=4, bird_list=None):
        # Create branches with zigzag layout (left to right, top to bottom)
        margin = 0
        upper_offset = 150
        id = 0
        x = 0
        y = 0
        row = 0
        left = True
        all_birds = []
        branches = []
        
        if bird_list == None: # Generate random birds (level is not custom)
            random_birds=[]
            # Create exactly MAX_BIRDS_PER_BRANCH birds of each color
            for color in constants.COLORS: # TODO: Make this dynamic
                for _ in range(max_birds_per_branch):
                    random_birds.append(Bird(color))
            random.shuffle(random_birds) # Shuffle all birds
            bird_index = 0
            for _ in range(num_branches):  # FIXME: Make this not hardcoded
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

        for _, branch_data in enumerate(all_birds):
            y = upper_offset + row * (constants.BRANCH_HEIGHT + 100)
            if left:
                x = margin
            else:
                x = constants.SCREEN_WIDTH - margin - constants.BRANCH_WIDTH
                row += 1
            branch = Branch(x, y, id)
            for color in branch_data:
                branch.add_bird(color)
            branches.append(branch)
            left = not left
            id += 1
            
        return branches
