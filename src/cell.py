from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing

from typing import List


class Cell:
    def __init__(self, x: int, y: int, updated: bool=False) -> None:
        self.updated = updated

        self.x = x
        self.y = y
        self.chemical = Nothing()
    
    def set(self, chemical: Chemical):
        self.chemical = chemical
    
    def delete(self):
        self.set(Nothing())
    
    def update(self, grid: List[List[Chemical]]) -> List[List[Chemical]]:
        if self.updated:
            print("True")
        if not self.updated:
            self.updated = True

            new = grid.copy()
            new = self.chemical.update(grid, self.x, self.y)

            return new
        
        return grid