from enum import Enum

from algorithms import dfs, dls, it_deep

class Algorithm(Enum):
    DFS = dfs.find_solution
    DLS = dls.find_solution
    IT_DEEP = it_deep.find_solution

class Solver():
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def find_solution(self, gameState):
        if self.algorithm:
            return self.algorithm(gameState)
        else:
            print(f"[ERROR!] algorithm '{self.algorithm}' not found!")