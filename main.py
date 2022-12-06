from typing import List
import pygame
from pygame.locals import *
from src.helpers import in_bounds

from src.constants import *

import random

pygame.init()
pygame.display.set_caption("Game")


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial" , 18 , bold = True)


def main():
    running = True

    spawning1 = False
    spawning2 = False
    spawning3 = False

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

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
                
            if event.type == KEYDOWN:
                if event.key == K_r:
                    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                elif event.key == K_SPACE:
                    spawning3 = True
            
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    spawning3 = False
            
            spawn(spawning1, spawning2, spawning3, grid)

        SCREEN.fill((150, 150, 150))

        draw(grid)
        update(grid)

        fps_counter()

        pygame.display.update()
        CLOCK.tick(1_000_000)


def spawn(spawning1: bool, spawning2: bool, spawning3: bool, grid):
    if spawning1:
        x = int((pygame.mouse.get_pos()[0] / WIDTH) * GRID_WIDTH)
        y = int((pygame.mouse.get_pos()[1] / HEIGHT) * GRID_HEIGHT)
        for cx in range(-3, 4):
            for cy in range(-3, 4):
                if in_bounds(x + cx, y + cy):
                    grid[y + cy][x + cx] = 1

    elif spawning2:
        x = int((pygame.mouse.get_pos()[0] / WIDTH) * GRID_WIDTH)
        y = int((pygame.mouse.get_pos()[1] / HEIGHT) * GRID_HEIGHT)
        for cx in range(-1, 2):
            for cy in range(-1, 2):
                if in_bounds(x + cx, y + cy):
                    grid[y + cy][x + cx] = 2
    
    elif spawning3:
        x = int((pygame.mouse.get_pos()[0] / WIDTH) * GRID_WIDTH)
        y = int((pygame.mouse.get_pos()[1] / HEIGHT) * GRID_HEIGHT)
        for cx in range(-1, 2):
            for cy in range(-1, 2):
                if in_bounds(x + cx, y + cy):
                    grid[y + cy][x + cx] = 4


def fps_counter():
    fps = str(int(CLOCK.get_fps()))
    fps_t = FONT.render(fps , 1, pygame.Color("RED"))
    SCREEN.blit(fps_t,(0,0))


def draw(grid: List[List[int]]):
    cell_size = WIDTH / GRID_WIDTH
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = (200, 200, 200)
            if grid[y][x] == 1:
                color = (0, 125, 255)
            elif grid[y][x] == 2:
                color = (127, 127, 0)
            elif grid[y][x] == 3:
                color = (200, 255, 75)
            elif grid[y][x] == 4:
                color = (255, 0, 0)

            pygame.draw.rect(SCREEN, color, (x * cell_size, y * cell_size, cell_size, cell_size))


def update(grid: List[List[int]]) -> List[List[int]]:
    for y in range(GRID_HEIGHT - 1, -1, -1):
        for x in range(GRID_HEIGHT):
            # ----- WATER -----
            if grid[y][x] == 1:
                if in_bounds(x, y + 1) and grid[y + 1][x] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x] = 1
                elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x + 1] = 1
                elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x - 1] = 1

                else:
                    rand_dir = 1 if random.random() > 0.5 else -1
                    if in_bounds(x + rand_dir, y) and grid[y][x + rand_dir] == 0:
                        grid[y][x] = 0
                        grid[y][x + rand_dir] = 1
                    elif in_bounds(x - rand_dir, y) and grid[y][x - rand_dir] == 0:
                        grid[y][x] = 0
                        grid[y][x - rand_dir] = 1
            
            # ----- SAND -----
            elif grid[y][x] == 2:
                if in_bounds(x, y + 1) and grid[y + 1][x] == 1:
                    grid[y][x] = 3
                    grid[y + 1][x] = 0
                if in_bounds(x, y - 1) and grid[y - 1][x] == 1:
                    grid[y][x] = 3
                    grid[y - 1][x] = 0

                elif in_bounds(x, y + 1) and grid[y + 1][x] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x] = 2
                elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x + 1] = 2
                elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x - 1] = 2

                elif in_bounds(x, y + 1) and grid[y + 1][x] == 1:
                    grid[y][x] = 1
                    grid[y + 1][x] = 2
                elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 1:
                    grid[y][x] = 1
                    grid[y + 1][x + 1] = 2
                elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 1:
                    grid[y][x] = 1
                    grid[y + 1][x - 1] = 2
            
            # ----- VOMIT -----
            elif grid[y][x] == 3:
                if in_bounds(x, y + 1) and grid[y + 1][x] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x] = 3
                elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x + 1] = 3
                elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 0:
                    grid[y][x] = 0
                    grid[y + 1][x - 1] = 3

                elif in_bounds(x, y + 1) and grid[y + 1][x] == 1:
                    grid[y][x] = 1
                    grid[y + 1][x] = 3
                elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 1:
                    grid[y][x] = 1
                    grid[y + 1][x + 1] = 3
                elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 1:
                    grid[y][x] = 1
                    grid[y + 1][x - 1] = 3
                    
                elif in_bounds(x, y + 1) and grid[y + 1][x] == 2:
                    grid[y][x] = 2
                    grid[y + 1][x] = 3
                elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 2:
                    grid[y][x] = 2
                    grid[y + 1][x + 1] = 3
                elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 2:
                    grid[y][x] = 2
                    grid[y + 1][x - 1] = 3


if __name__ == "__main__":
    main()