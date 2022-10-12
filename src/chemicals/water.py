from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.helpers import in_bounds, is_empty, is_equal, touching
from src.constants import *

from typing import List
import random


class Water(Chemical):
    color = (0, 127, 255)

    density = 1

    spread_rate = 3

    def update(self, grid: List[List[Chemical]], x: int, y: int) -> List[List[Chemical]]:
        new = grid.copy()

        for i in range(GRAVITY):
            for j in range(self.spread_rate, 0, -1):
                if in_bounds(x - j, y + i) and is_empty(grid[x - j][y + i].chemical):
                    new[x][y].set(new[x - j][y + i].chemical)
                    new[x - j][y + i].set(Water())
                    break

                if in_bounds(x + j, y + i) and is_empty(grid[x + j][y + i].chemical):
                    new[x][y].set(new[x + j][y + i].chemical)
                    new[x - j][y + i].set(Water())
                    break
            else:
                break

        return new