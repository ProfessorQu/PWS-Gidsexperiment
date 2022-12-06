from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.chemicals.water import Water
from src.helpers import in_bounds, less_dense, is_empty
from src.constants import *

from typing import List


class Sand(Chemical):
    color = (127, 127, 0)

    density = 2

    def update(self, grid: List[List[Chemical]], x: int, y: int) -> List[List[Chemical]]:
        new = grid.copy()
        
        fallen = False
        i = GRAVITY

        # while i > 0 and not fallen:
        if in_bounds(x, y + 1) and less_dense(self, grid[x][y + 1].chemical):
            # if not is_empty(grid[x][y + 1].chemical):
            #     new[x][y].set(grid[x][y + 1].chemical)
            #     new[x][y + 1].set(self)
            # else:
            new[x][y].set(grid[x][y + 1].chemical)
            new[x][y + 1].set(self)

            fallen = True

        # elif in_bounds(x + 1, y + 1) and less_dense(self, grid[x + 1][y + 1].chemical):
        #     new[x + 1][y - 1].set(grid[x + 1][y + 1].chemical)
        #     new[x][y].set(Nothing())
        #     new[x + 1][y + 1].set(self)
            
        #     fallen = True
        
        # elif in_bounds(x - 1, y + 1) and less_dense(self, grid[x - 1][y + 1].chemical):
        #     new[x - 1][y - 1].set(grid[x - 1][y + 1].chemical)
        #     new[x][y].set(Nothing())
        #     new[x - 1][y + 1].set(self)

        #     fallen = True

            i -= 1
        
        return new
