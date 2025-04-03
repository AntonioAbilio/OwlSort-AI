import ast
import tkinter as tk
from tkinter import filedialog
from collections import Counter
import constants
from models.bird import Bird
from levels.level_generator import LevelGenerator
import os
import threading


# Function to open file dialog and load level
def load_level(callback):

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select Level File",
        filetypes=[("Text Files", "*.txt")]
    )
    if not file_path or not os.path.exists(file_path):
        print("File does not exist or no file selected.")
        callback(None)
        root.destroy()
        return
    
    with open(file_path, 'r') as file:
        content = file.read().strip()  # Read and strip unnecessary whitespaces
        try:
            rgb_list = ast.literal_eval(content)
            levelGenerator = LevelGenerator()
            (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(file_path)
            if color_counts is not None:
                callback ((level, color_counts, max_birds_per_branch))
            else:
                print("Invalid level: Number of birds per color is not balanced.")
                callback(None)
                root.destroy()
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing file: {e}")
            callback(None)
            root.destroy()

# Run the file dialog and processing in a separate thread
def load_level_threaded(callback):
    threading.Thread(target=lambda: load_level(callback)).start()

def parse_level(level_data):
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

    # Check if all colors have exactly x occurrences
    valid = all(count == list(color_counts.values())[0] for count in color_counts.values())
    
    max_branch_size = 0
    for branch in rgb_list:
        if len(branch) > max_branch_size:
            max_branch_size = len(branch)
    
    if valid:
        return len(color_counts), max_branch_size
    return None
    

def check_level_possible(gameState):
    pass
