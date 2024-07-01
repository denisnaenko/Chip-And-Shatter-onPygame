from settings import *
from random import randint

class CRT:
    def __init__(self):
        self.tv = pygame.image.load(join('images', 'effects', 'tv.png')).convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = pygame.display.get_surface()

        # Create a surface for CRT lines
        self.crt_lines = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.create_crt_lines()

    def create_crt_lines(self, color='black'):
        line_height = 3
        line_amount = WINDOW_HEIGHT // line_height

        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.crt_lines, color, (0, y_pos), (WINDOW_WIDTH, y_pos), 1)

    def draw_crt(self):
        self.tv.set_alpha(randint(70, 90))
        self.screen.blit(self.tv, (0, 0))
        self.screen.blit(self.crt_lines, (0, 0))
