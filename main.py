import itertools
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


left = False

def main():
    running = True

    spawning1 = False
    spawning2 = False
    removing = False

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    spawning1 = True
                elif event.button == 2:
                    removing = True
                elif event.button == 3:
                    spawning2 = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    spawning1 = False
                elif event.button == 2:
                    removing = False
                elif event.button == 3:
                    spawning2 = False

            if event.type == KEYDOWN and event.key == K_r:
                grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

            spawn(spawning1, spawning2, removing, grid)

        SCREEN.fill((150, 150, 150))

        draw(grid)
        update(grid)

        fps_counter()

        pygame.display.update()
        CLOCK.tick(1_000_000)


def spawn(spawning1: bool, spawning2: bool, removing: bool, grid):
    if removing:
        set_square(-4, 5, 0, grid)
    elif spawning1:
        set_square(-3, 4, 1, grid)
    elif spawning2:
        set_square(-1, 2, 2, grid)


def set_square(lower_bound, upper_bound, type, grid):
    x = int((pygame.mouse.get_pos()[0] / WIDTH) * GRID_WIDTH)
    y = int((pygame.mouse.get_pos()[1] / HEIGHT) * GRID_HEIGHT)
    for cx, cy in itertools.product(range(lower_bound, upper_bound), range(lower_bound, upper_bound)):
        if in_bounds(x + cx, y + cy):
            grid[y + cy][x + cx] = type


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
    global left

    if left:
        update_left(grid)
    else:
        update_right(grid)
    
    left = not left

def update_left(grid: List[List[int]]) -> List[List[int]]:
    for y, x in itertools.product(range(GRID_HEIGHT - 1, -1, -1), range(GRID_HEIGHT)):
        # ----- WATER -----
        if grid[y][x] == 1:
            update_water(grid, x, y)

        # ----- SAND -----
        elif grid[y][x] == 2:
            update_sand(grid, x, y)

        # ----- PRODUCT -----
        elif grid[y][x] == 3:
            update_product(grid, x, y)

def update_right(grid: List[List[int]]) -> List[List[int]]:
    for y, x in itertools.product(range(GRID_HEIGHT - 1, -1, -1), range(GRID_HEIGHT - 1, -1, -1)):
        # ----- WATER -----
        if grid[y][x] == 1:
            update_water(grid, x, y)

        # ----- SAND -----
        elif grid[y][x] == 2:
            update_sand(grid, x, y)

        # ----- PRODUCT -----
        elif grid[y][x] == 3:
            update_product(grid, x, y)


def update_water(grid: List[List[int]], x: int, y: int):
    updated = water_fall(grid, x, y)

    if not updated:
        water_spread(grid, x, y)

def water_fall(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 0:
        grid[y][x] = 0
        grid[y + 1][x] = 1

        return True
    elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 0:
        grid[y][x] = 0
        grid[y + 1][x + 1] = 1

        return True
    elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 0:
        grid[y][x] = 0
        grid[y + 1][x - 1] = 1

        return True

def water_spread(grid: List[List[int]], x: int, y: int) -> bool:
    rand_dir = 1 if random.random() > 0.5 else -1
    if in_bounds(x + rand_dir, y) and grid[y][x + rand_dir] == 0:
        grid[y][x] = 0
        grid[y][x + rand_dir] = 1

        return True
    elif in_bounds(x - rand_dir, y) and grid[y][x - rand_dir] == 0:
        grid[y][x] = 0
        grid[y][x - rand_dir] = 1
            
        return True

def update_sand(grid: List[List[int]], x: int, y: int):
    updated = sand_react(grid, x, y)

    if not updated:
        updated = sand_fall(grid, x, y)
    
    if not updated:
        sand_fall_in_water(grid, x, y)

def sand_react(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 1:
        grid[y][x] = 3
        grid[y + 1][x] = 0

        return True
    if in_bounds(x, y - 1) and grid[y - 1][x] == 1:
        grid[y][x] = 3
        grid[y - 1][x] = 0
        
        return True

def sand_fall(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 0:
        grid[y][x] = 0
        grid[y + 1][x] = 2

        return True
    elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 0:
        grid[y][x] = 0
        grid[y + 1][x + 1] = 2
        
        return True
    elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 0:
        grid[y][x] = 0
        grid[y + 1][x - 1] = 2
        
        return True

def sand_fall_in_water(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 1:
        grid[y][x] = 1
        grid[y + 1][x] = 2
        
        return True
    elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 1:
        grid[y][x] = 1
        grid[y + 1][x + 1] = 2
        
        return True
    elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 1:
        grid[y][x] = 1
        grid[y + 1][x - 1] = 2
        
        return True

def update_product(grid: List[List[int]], x: int, y: int):
    updated = product_fall(grid, x, y)

    if not updated:
        updated = product_fall_in_water(grid, x, y)
    
    if not updated:
        product_fall_in_sand(grid, x, y)

def product_fall(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 0:
        grid[y][x] = 0
        grid[y + 1][x] = 3

        return True
    elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 0:
        grid[y][x] = 0
        grid[y + 1][x + 1] = 3

        return True
    elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 0:
        grid[y][x] = 0
        grid[y + 1][x - 1] = 3

        return True

def product_fall_in_water(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 1:
        grid[y][x] = 1
        grid[y + 1][x] = 3

        return True
    elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 1:
        grid[y][x] = 1
        grid[y + 1][x + 1] = 3

        return True
    elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 1:
        grid[y][x] = 1
        grid[y + 1][x - 1] = 3

        return True

def product_fall_in_sand(grid: List[List[int]], x: int, y: int) -> bool:
    if in_bounds(x, y + 1) and grid[y + 1][x] == 2:
        grid[y][x] = 2
        grid[y + 1][x] = 3

        return True
    elif in_bounds(x + 1, y + 1) and grid[y + 1][x + 1] == 2:
        grid[y][x] = 2
        grid[y + 1][x + 1] = 3

        return True
    elif in_bounds(x - 1, y + 1) and grid[y + 1][x - 1] == 2:
        grid[y][x] = 2
        grid[y + 1][x - 1] = 3

        return True


if __name__ == "__main__":
    main()