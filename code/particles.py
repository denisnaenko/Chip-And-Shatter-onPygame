from settings import *
from random import uniform

class Sparkles(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 100, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        self.lifetime = 60

    def update(self, dt):
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()
