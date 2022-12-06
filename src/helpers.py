from src.constants import *

from typing import List, Tuple

def in_bounds(x: int, y: int) -> bool:
    return y >= 0 and y < GRID_HEIGHT and x >= 0 and x < GRID_WIDTH
