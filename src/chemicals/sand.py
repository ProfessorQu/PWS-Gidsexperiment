from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.chemicals.water import Water
from src.helpers import in_bounds, is_empty, is_equal, touching
from src.constants import *

from typing import List


class Sand(Chemical):
    color = (127, 127, 0)

    density = 2

    def update(self, grid: List[List[Chemical]], x: int, y: int) -> List[List[Chemical]]:
        new = grid.copy()

        new_x, new_y = x, y
        
        for _ in range(1, GRAVITY):
            if in_bounds(new_x, new_y + 1) and is_empty(grid[new_x][new_y + 1].chemical):
                new[new_x][new_y].set(Nothing())
                new[new_x][new_y + 1].set(Sand())
                new_y += 1

            elif in_bounds(new_x + 1, new_y + 1) and is_empty(grid[new_x + 1][new_y + 1].chemical):
                new[new_x][new_y].set(Nothing())
                new[new_x + 1][new_y + 1].set(Sand())
                new_x += 1
                new_y += 1
            
            elif in_bounds(new_x - 1, new_y + 1) and is_empty(grid[new_x - 1][new_y + 1].chemical):
                new[new_x][new_y].set(Nothing())
                new[new_x - 1][new_y + 1].set(Sand())
                new_x -= 1
                new_y += 1
        
        return new
