import tkinter as tk
from tkinter import filedialog
from levels.level_generator import LevelGenerator
import os
import threading

# Function to open file dialog and load level
def load_level(callback):

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select Level File",
        filetypes=[("Text Files", "*.txt"), ("CuCu Files", "*.cucu")],
    )
    if not file_path or not os.path.exists(file_path):
        print("File does not exist or no file selected.")
        callback(None)
        root.destroy()
        return

    try:
        levelGenerator = LevelGenerator()
        result = levelGenerator.generate_level_from_file(file_path)
        if result is None:
            callback(None)
            root.destroy()
        else:
            (level, color_counts, max_birds_per_branch) = result
            callback ((level, color_counts, max_birds_per_branch))
            root.destroy()
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing file: {e}")
        callback(None)
        root.destroy()

# Run the file dialog and processing in a separate thread
def load_level_threaded(callback):
    threading.Thread(target=lambda: load_level(callback)).start()
