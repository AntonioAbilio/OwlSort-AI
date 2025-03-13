import ast
import tkinter as tk
from tkinter import filedialog
from collections import Counter
from models.bird import Bird
import os

# Function to open file dialog and load level
def load_level():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select Level File",
        filetypes=[("Text Files", "*.txt")]
    )
    
    if not os.path.exists(file_path):
        print("File does not exist.")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read().strip()  # Read and strip unnecessary whitespaces
        # Convert the string representation into list of lists
        try:
            rgb_list = ast.literal_eval(content)
            branches = parse_level(rgb_list)
            color_counts = validate_birds(rgb_list)
            if color_counts is not None:
                return (color_counts, branches)
            else:
                print("Invalid level: Each color must appear exactly 4 times.")
                return None
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing file: {e}")
            return None

def parse_level(level_data) :
    branches = []
    for branch_data in level_data:
        branch = []
        for bird_color in branch_data:
            bird = Bird(bird_color)
            branch.append(bird)
        branches.append(branch)
    return branches

def validate_birds(rgb_list):
    flat_list = [color for row in rgb_list for color in row]  # Flatten the nested list
    color_counts = Counter(flat_list)

    # Check if all colors have exactly 4 occurrences
    valid = all(count == 4 for count in color_counts.values())
    
    if valid:
        return len(color_counts)
    return None
    

def check_level_possible(gameState):
    pass
    