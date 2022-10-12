from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.helpers import in_bounds, is_empty, is_equal, touching
from src.constants import *

from typing import List


class Sand(Chemical):
    color = (127, 127, 0)

    density = 2

    def update(self, grid: List[List[Chemical]], x: int, y: int) -> List[List[Chemical]]:
        new = grid.copy()
        
        found = False
        i = GRAVITY

        while i > 0 and not found:
            if in_bounds(x, y  + i) and is_empty(grid[x][y + i].chemical):
                new[x][y].set(Nothing())
                new[x][y + i].set(Sand())

                found = True

            elif in_bounds(x + 1, y + i) and is_empty(grid[x + 1][y  + i].chemical):
                new[x][y].set(Nothing())
                new[x + 1][y + i].set(Sand())
                
                found = True
            
            elif in_bounds(x - 1, y + i) and is_empty(grid[x - 1][y + i].chemical):
                new[x][y].set(Nothing())
                new[x - 1][y + i].set(Sand())
                
                found = True

            i -= 1
        
        return new
