import os
import psutil
import threading
import threading
import csv

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.vms

def get_thread_id():
    return threading.current_thread().ident

def get_all_thread_ids():
    return [thread.ident for thread in threading.enumerate()]

def print_statistics(current_path = [], algorithmName = "", states_checked = 0, elapsed_time = 0, current_memory_usage = 0, starting_memory_usage = 0, solutionFound = False):
    import os.path
    
    memory_used = (current_memory_usage - starting_memory_usage) / (10**6)
    
    # Print statistics to console
    if (solutionFound):
        print(f"Solution found! Path length: {len(current_path)}")
        print(f"{algorithmName} stats: {states_checked} states checked")
        print(f"Time taken: {elapsed_time:.5f} seconds")
        print(f"Total amount of memory used: {memory_used} MBytes")
    else:
        #TODO: Should we display the other stats too even when we did not find a path?
        print("No solution found")
        print(f"Time taken: {elapsed_time:.5f} seconds")
    
    # Save statistics to CSV file
    file_exists = os.path.isfile('statistics.csv')
    
    with open('statistics.csv', 'a', newline='') as csvfile:
        fieldnames = ['Algorithm', 'Solution Found', 'Path Length', 'States Checked', 'Elapsed Time (s)', 'Memory Used (MB)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Algorithm': algorithmName,
            'Solution Found': solutionFound,
            'Path Length': len(current_path) if solutionFound else 'N/A',
            'States Checked': states_checked,
            'Elapsed Time (s)': round(elapsed_time, 5),
            'Memory Used (MB)': round(memory_used, 2)
        })