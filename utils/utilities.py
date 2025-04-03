import os
import psutil

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def print_statistics(current_path = [], algorithmName = "", states_checked = 0, elapsed_time = 0, current_memory_usage = 0, starting_memory_usage = 0, solutionFound = False):
    if (solutionFound):
        print(f"Solution found! Path length: {len(current_path)}")
        print(f"{algorithmName} stats: {states_checked} states checked")
        print(f"Time taken: {elapsed_time:.5f} seconds")
        print(f"Total amount of memory used: {(current_memory_usage - starting_memory_usage) / (10**6)} MBytes")
        return
    # Should we display the other stats too even when we did not find a path ?
    print("No solution found")
    print(f"Time taken: {elapsed_time:.5f} seconds")