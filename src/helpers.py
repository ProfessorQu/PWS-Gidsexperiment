from src.chemicals.chemical import Chemical
from src.chemicals.nothing import Nothing
from src.constants import *

from typing import List, Tuple

def in_bounds(x: int, y: int) -> bool:
    return y >= 0 and y < GRID_HEIGHT and x >= 0 and x < GRID_WIDTH

def is_equal(test: Chemical, tester: Chemical) -> bool:
    return isinstance(test, tester)

def is_empty(test: Chemical) -> bool:
    return is_equal(test, Nothing)

def touching(grid: List[List[Chemical]], x: int, y: int, tester: Chemical) -> Tuple[int, int]:
    left    =   in_bounds(x - 1, y) and is_equal(grid[x - 1][y].chemical, tester)
    right   =   in_bounds(x + 1, y) and is_equal(grid[x + 1][y].chemical, tester)
    top     =   in_bounds(x, y - 1) and is_equal(grid[x][y - 1].chemical, tester)

    if in_bounds(x, y + 1) and is_equal(grid[x][y + 1].chemical, tester):
        return (0, 1)
    if left:
        return (-1, 0)
    if right:
        return (1, 0)

    return (0, -1) if top else (0, 0)