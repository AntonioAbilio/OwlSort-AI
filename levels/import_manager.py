import pygame
import json
import ast
import tkinter as tk
from tkinter import filedialog
import ctypes
from models.branch import Branch
from models.bird import Bird

# Function to open file dialog and load level
def load_level():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select Level File",
        filetypes=[("Text Files", "*.txt")]
    )
    
    with open(file_path, 'r') as file:
        content = file.read().strip()  # Read and strip unnecessary whitespaces
        # Convert the string representation into list of lists
        try:
            rgb_list = ast.literal_eval(content)
            branches = parse_level(rgb_list)
            for branch in branches:
                for bird in branch:
                    print(bird.color)
            return rgb_list
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
    

def check_level_possible(GameState):
    pass
    