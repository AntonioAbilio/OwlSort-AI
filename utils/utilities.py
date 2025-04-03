import os
import psutil
import threading
import threading

def process_memory():
    # TODO: remove
    print(f"tid {get_thread_id()}")

    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.vms

def get_thread_id():
    return threading.current_thread().ident

def get_all_thread_ids():
    return [thread.ident for thread in threading.enumerate()]

def print_statistics(current_path = [], algorithmName = "", states_checked = 0, elapsed_time = 0, current_memory_usage = 0, starting_memory_usage = 0, solutionFound = False):
    if (solutionFound):
        print(f"Solution found! Path length: {len(current_path)}")
        print(f"{algorithmName} stats: {states_checked} states checked")
        print(f"Time taken: {elapsed_time:.5f} seconds")
        print(f"Total amount of memory used: {(current_memory_usage - starting_memory_usage) / (10**6)} MBytes")
        return
    #TODO: Should we display the other stats too even when we did not find a path ?
    print("No solution found")
    print(f"Time taken: {elapsed_time:.5f} seconds")