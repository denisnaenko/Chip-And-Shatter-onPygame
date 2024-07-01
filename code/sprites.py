from settings import *
from particles import Sparkles

class PlatformSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        # alpha-channel
        self.alpha = 0
        self.appearing = True

    def update(self, dt):
        if self.appearing:
            self.alpha += 255 * dt
            if self.alpha >= 255:
                self.alpha = 255
                self.appearing = False
            self.image.set_alpha(self.alpha)

class KillLineSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, groups):
        super().__init__(groups)
        
        self.image = pygame.Surface((width, height))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=(0, 0))
        self.vel_x = 100

    def update(self, dt):
        self.rect.x += self.vel_x * dt

class BorderLineSprite(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, groups):
        super().__init__(groups)
        self.image = pygame.Surface((width, height))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)
    
    def update(self, dt):
        self.rect.x += 100 * dt

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'enemies', 'bat', '0.png'))
        self.rect = self.image.get_rect(topleft=pos)

        # particles setup
        self.particle_timer = 0
        self.particle_interval = 30

        self.frames, self.frame_index = frames, 0

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)
        self.rect.x -= 1 * dt

        # emit particles
        self.particle_timer += 1
        if self.particle_timer >= self.particle_interval:
            Sparkles(self.rect.center, self.groups())
            self.particle_timer = 0