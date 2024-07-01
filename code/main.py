from settings import *
from support import *
from level import Level
from sys import exit

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Chip & Shatter')
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.running = True

        self.level = Level(self.level_frames)

    def import_assets(self):
        self.level_frames = {
            'player': import_sub_folders('images', 'player'),
            'enemy': import_folder('images', 'enemies', 'bat')
        }   

    def run(self):          
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.level.run(dt, self.level_frames)

            pygame.display.update()

        pygame.quit()   
        exit()


if __name__ == '__main__':
    game = Game()
    game.run()  