from enum import Enum

from states.gameState import GameState
from algorithms import bfs, dfs, dls, astar, it_deep, wastar, greedy
import threading
import time


class Algorithm(Enum):
    BFS     = bfs.find_solution
    DFS_FIRST_ACCEPT = dfs.find_solution
    DFS_BEST         = lambda game_state: dfs.find_solution(game_state, first_accept=False)
    DLS     = dls.find_solution
    ASTAR   = astar.find_solution
    WASTAR  = wastar.find_solution
    IT_DEEP = it_deep.find_solution
    GREEDY  = greedy.find_solution



class Solver:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.solution = None
        self.is_running = False
        self.thread = None
        self.start_time = None
        self.algorithm_name = None
        
        # For algorithm that's currently running
        for alg in Algorithm:
            if alg.value == algorithm:
                self.algorithm_name = alg.name
                break
    
    def _run_algorithm(self, game_state, callback):
        """Internal method to run the algorithm in a thread"""
        try:
            solution = self.algorithm(game_state)
            self.solution = solution
            self.is_running = False
            self.start_time = None
            
            # Call the callback with the solution if one was provided
            if callback:
                callback(solution, self.algorithm)
                
        except Exception as e:
            print(f"[ERROR!] Solve Algorithm error: {e}")
            self.solution = []
            self.is_running = False
            self.start_time = None
            
            # Call the callback with empty solution if there was an error
            if callback:
                callback([])
    
    def find_solution(self, game_state, callback=None):
        """
        Start solving in a background thread.
        
        Args:
            game_state: The game state to solve
            callback: Optional function to call when solution is found
                      The callback will receive the solution as parameter
        
        Returns:
            True if solving started, False if already running
        """
        assert isinstance(game_state, GameState)
        assert isinstance(game_state.move_history, list)
        
        # Don't start a new thread if one is already running
        if self.is_running:
            return False
            
        self.is_running = True
        self.solution = None
        self.start_time = time.time()  # Record when we started
        self.thread = threading.Thread(
            target=self._run_algorithm,
            args=(game_state, callback)
        )
        self.thread.daemon = True  # Make thread exit when main program exits
        self.thread.start()
        return True
    
    def is_solution_ready(self):
        """Check if the solution is ready"""
        return not self.is_running and self.solution is not None
    
    def get_solution(self):
        """Get the current solution (may be None if not ready)"""
        return self.solution
    
    def get_elapsed_time(self):
        """Get the elapsed time since the algorithm started running"""
        if not self.is_running or self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def cancel(self):
        """
        Flag to cancel solving (note: this doesn't actually stop the thread,
        but the algorithm should check for this flag and stop early)
        """
        self.is_running = False
        self.start_time = None