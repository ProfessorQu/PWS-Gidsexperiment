from typing import List


class Chemical:
    density = -1

    def update(self, grid: List[List['Chemical']], x: int, y: int) -> List[List['Chemical']]:
        raise NotImplementedError()