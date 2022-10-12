from typing import List
import pygame
from pygame.locals import *
from src.chemicals.chemical import Chemical

from src.constants import *
from src.cell import Cell
from src.chemicals.nothing import Nothing
from src.chemicals.water import Water
from src.chemicals.sand import Sand

import random

pygame.init()
pygame.display.set_caption("Game")


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


def main():
    running = True

    spawning1 = False
    spawning2 = False

    grid = [[Cell(y, x) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    spawning1 = True
                elif event.button == 3:
                    spawning2 = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    spawning1 = False
                elif event.button == 3:
                    spawning2 = False


        if spawning1:
            x = int((pygame.mouse.get_pos()[0] / WIDTH) * GRID_WIDTH)
            y = int((pygame.mouse.get_pos()[1] / HEIGHT) * GRID_HEIGHT)
            for cx in range(-3, 4):
                for cy in range(-3, 4):
                    grid[x + cx][y + cy].set(Water())

        elif spawning2:
            x = int((pygame.mouse.get_pos()[0] / WIDTH) * GRID_WIDTH)
            y = int((pygame.mouse.get_pos()[1] / HEIGHT) * GRID_HEIGHT)
            for cx in range(-1, 2):
                for cy in range(-1, 2):
                    grid[x + cx][y + cy].set(Sand())

        SCREEN.fill((150, 150, 150))

        draw(grid)
        grid = update(grid)
        grid = reset(grid)

        pygame.display.update()
        CLOCK.tick(60)

def draw(grid: List[List[Chemical]]):
    cell_size = WIDTH / GRID_WIDTH
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(SCREEN, grid[x][y].chemical.color, (x * cell_size, y * cell_size, cell_size, cell_size))

def update(grid: List[List[Chemical]]) -> List[List[Chemical]]:
    new = grid.copy()
    
    for y in range(GRID_HEIGHT - 1, -1, -1):
        for x in range(GRID_WIDTH):
            if not isinstance(grid[x][y].chemical, Nothing):
                new = grid[x][y].update(grid)

    return new

def reset(grid: List[List[Chemical]]) -> List[List[Chemical]]:
    new = grid.copy()
    
    for y in range(GRID_HEIGHT - 1, -1, -1):
        for x in range(GRID_WIDTH):
            grid[x][y].updated = False
            new[x][y].updated = False

    return new

if __name__ == "__main__":
    main()