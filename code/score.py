from settings import *

class Score:
    def __init__(self, font):
        self.font = font
        self.display_surf = pygame.display.get_surface()

    def display_score(self, start_time):
        cur_time = pygame.time.get_ticks() // 10 - start_time
        score_surf = self.font.render(f'{cur_time}', False, 'white')
        score_rect = score_surf.get_rect(center = (100, 50))
        
        self.display_surf.blit(score_surf, score_rect)
