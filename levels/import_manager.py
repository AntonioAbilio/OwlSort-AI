import ast
import tkinter as tk
from tkinter import filedialog
from collections import Counter
import constants
from models.bird import Bird
from levels.level_generator import LevelGenerator
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
            levelGenerator = LevelGenerator()
            (level, color_counts, max_birds_per_branch) = levelGenerator.generate_level_from_file(file_path)
            if color_counts is not None:
                return (level, color_counts, max_birds_per_branch)
            else:
                print("Invalid level: Number of birds per color is not balanced.")
                return None
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing file: {e}")
            return None
    