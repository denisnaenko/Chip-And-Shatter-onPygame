from random import random
import pygame
from settings import *

class Cellural_Automata:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = None

        self.surf_img = pygame.image.load(join('images', 'tiles', 'tile.png')).convert_alpha()
        self.platforms = []

    def initialize_grid(self, fill_prob=0.4):
        self.grid = [[1 if random() < fill_prob else 0 for _ in range(self.width)] for _ in range(self.height)]

    def count_alive_neighbors(self, x, y):
        alive_neighbors = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    alive_neighbors += self.grid[ny][nx]
        return alive_neighbors

    def apply_cellular_automata(self, steps=4):
        width, height = len(self.grid[0]), len(self.grid)
        for _ in range(steps):
            new_grid = [[0 for _ in range(width)] for _ in range(height)]
            for y in range(height):
                for x in range(width):
                    alive_neighbors = self.count_alive_neighbors(x, y)
                    if self.grid[y][x] == 1:
                        new_grid[y][x] = 1 if alive_neighbors >= 4 else 0
                    else:
                        new_grid[y][x] = 1 if alive_neighbors >= 5 else 0
            self.grid = new_grid

    def generate_platforms_from_grid(self, offset_x=0):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    surf = self.surf_img
                    self.platforms.append((x * TILE_SIZE + offset_x, y * TILE_SIZE, surf))

    def generate_level(self, offset_x=0):
        self.initialize_grid()
        self.apply_cellular_automata()
        self.generate_platforms_from_grid(offset_x)

        return self.platforms