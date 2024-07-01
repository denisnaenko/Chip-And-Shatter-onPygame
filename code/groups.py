from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        for sprite in self:
            offset_pos = (sprite.rect.topleft[0] + self.offset.x,
                          sprite.rect.topleft[1] + self.offset.y)
            
            self.display_surface.blit(sprite.image, offset_pos)