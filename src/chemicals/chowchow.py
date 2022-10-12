from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.helpers import in_bounds, is_equal

import random
from typing import List


class Chowchow(Chemical):
    color = (255, 255, 0)

    density = 0.05

    def update(self, grid: List[List[Chemical]], x: int, y: int) -> List[List[Chemical]]:
        new = grid.copy()

        # if in_bounds(x, y + 1) and is_equal(grid[x][y + 1].chemical, Nothing):
        #     new[x][y].set(grid[x][y + 1].chemical)
        #     new[x][y + 1].set(Chowchow())

        # if in_bounds(x + 1, y + 1) and is_equal(grid[x + 1][y + 1].chemical, Nothing):
        #     new[x][y].set(grid[x + 1][y - 1].chemical)
        #     new[x + 1][y + 1].set(Chowchow())

        # if in_bounds(x - 1, y + 1) and is_equal(grid[x - 1][y + 1].chemical, Nothing):
        #     new[x][y].set(grid[x - 1][y + 1].chemical)
        #     new[x - 1][y + 1].set(Chowchow())

        return new