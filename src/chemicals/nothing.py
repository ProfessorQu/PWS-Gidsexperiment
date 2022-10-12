from src.chemicals.chemical import Chemical

from typing import List


class Nothing(Chemical):
    color = (200, 200, 200)

    density = 0.1

    def update(self, grid: List[List[Chemical]], x: int, y: int) -> List[List[Chemical]]:
        return grid