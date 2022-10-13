from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.helpers import in_bounds, is_empty, is_equal, touching
from src.cell import Cell
from src.constants import *

from typing import List
import random


class Water(Chemical):
    color = (0, 127, 255)

    density = 1

    SPREAD_RATE = 10

    def update(self, grid: List[List[Cell]], x: int, y: int) -> List[List[Cell]]:
        new = grid.copy()

        fallen = False
        i = GRAVITY

        while i > 0 and not fallen:
            if in_bounds(x, y + i) and is_empty(grid[x][y + i].chemical):
                new[x][y].set(Nothing())
                new[x][y + i].set(Water())

                fallen = True

            elif in_bounds(x + 1, y + i) and is_empty(grid[x + 1][y  + i].chemical):
                new[x][y].set(Nothing())
                new[x + 1][y + i].set(Water())
                
                fallen = True
            
            elif in_bounds(x - 1, y + i) and is_empty(grid[x - 1][y + i].chemical):
                new[x][y].set(Nothing())
                new[x - 1][y + i].set(Water())
                
                fallen = True

            i -= 1
        
        if not fallen:
            spread = False
            j = self.SPREAD_RATE

            rand_dir = 1 if random.random() > 0.5 else -1

            while j > 0 and not spread:
                if in_bounds(x + j * rand_dir, y) and is_empty(grid[x + j * rand_dir][y].chemical):
                    new[x][y].set(Nothing())
                    new[x + j * rand_dir][y].set(Water())
                    
                    spread = True
                
                elif in_bounds(x - j * rand_dir, y) and is_empty(grid[x - j * rand_dir][y].chemical):
                    new[x][y].set(Nothing())
                    new[x - j * rand_dir][y].set(Water())
                    
                    spread = True
                
                j -= 1

        return new