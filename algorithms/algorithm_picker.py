from enum import Enum
from states.gameState import GameState
from algorithms import bfs, dfs, dls, astar

class Algorithm(Enum):
    BFS     = bfs.find_solution
    DFS     = dfs.find_solution
    DLS     = dls.find_solution
    ASTAR   = astar.find_solution

class Solver():
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def find_solution(self, game_state):
        assert isinstance(game_state, GameState)
        assert isinstance(game_state.move_history, list)
        if self.algorithm:
            return self.algorithm(game_state)
        else:
            print(f"[ERROR!] algorithm '{self.algorithm}' not found!")