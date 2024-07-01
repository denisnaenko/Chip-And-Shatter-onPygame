from settings import *
from ca_algorithm import Cellural_Automata
from sprites import PlatformSprite, KillLineSprite, BorderLineSprite, EnemySprite
from player import Player
from groups import AllSprites
from score import Score
from random import randint
from crt_effect import CRT

class Level:
    def __init__(self, level_frames):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(join('font', 'Pixeltype.ttf'), 60)
        self.game_active = True
        self.start_time = 0

        # score
        self.score = Score(self.font)

        # level setup
        self.level_width = 40
        self.level_height = WINDOW_HEIGHT // TILE_SIZE

        # cellural automata init
        self.CA = Cellural_Automata(self.level_width, self.level_height)

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.border_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        # offset
        self.scroll_offset = 0
        self.scroll_threshold = WINDOW_WIDTH / 2

        # platforms
        self.platforms = []
        self.setup(level_frames)

        # kill-line
        self.kill_line = KillLineSprite(2, WINDOW_HEIGHT, self.all_sprites)

        # CRT
        self.crt = CRT()

    def setup(self, level_frames):
        # generate platforms
        platforms = self.CA.generate_level()
        for x, y, surf in platforms:
            PlatformSprite((x, y), surf, groups=(self.all_sprites, self.collision_sprites))
            self.platforms.append((x, y, surf))

        # generate enemies
        for _ in range(ENEMY_COUNT):  # initial enemy count
            x = randint(600, 1000) + self.scroll_offset
            y = randint(50, 680)
            EnemySprite((x, y), (self.all_sprites, self.enemies, self.particles), frames=level_frames['enemy'])

        # player
        self.player_start_pos = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        self.player = Player(
            pos=self.player_start_pos, 
            groups=self.all_sprites,
            collision_sprites=self.collision_sprites,
            frames=level_frames['player'])
        
        # border-lines
        self.top_wall = BorderLineSprite((0, -30), WINDOW_WIDTH * 2, 30, (self.all_sprites, self.border_sprites))
        self.bottom_wall = BorderLineSprite((0, WINDOW_HEIGHT), WINDOW_WIDTH * 2, 30, (self.all_sprites, self.border_sprites))

    def generate_new_platforms(self):
        last_x = max([platform[0] for platform in self.platforms]) // TILE_SIZE
        platforms = self.CA.generate_level(last_x * TILE_SIZE)
        for x, y, surf in platforms:
            PlatformSprite((x, y), surf, groups=(self.all_sprites, self.collision_sprites))
            self.platforms.append((x, y, surf))

    def generate_new_enemies(self, level_frames):
        x = max([enemy.rect.x for enemy in self.enemies.sprites()]) + randint(600, 1000)
        y = randint(50, 680)
        EnemySprite((x, y), (self.all_sprites, self.enemies, self.particles), frames=level_frames['enemy'])

    def remove_old_sprites(self):
        self.platforms = [(x, y, surf) for x, y, surf in self.platforms if x > self.scroll_offset - TILE_SIZE]
        for sprite in self.all_sprites:
            if sprite not in self.border_sprites and (sprite.rect.left < self.kill_line.rect.left or 
                                                    sprite.rect.bottom > self.bottom_wall.rect.top or 
                                                    sprite.rect.top < self.top_wall.rect.bottom):
                sprite.kill()

    def check_player_death(self):
        if pygame.sprite.spritecollide(self.player, [self.kill_line ,self.bottom_wall, self.top_wall], False) or pygame.sprite.spritecollideany(self.player, self.enemies):
            self.game_active = False
    
    def player_attack(self):
        if self.player.state in {'attack', 'attack-jump', 'attack-crouch'}:
            collided_sprite = pygame.sprite.spritecollideany(self.player, self.enemies)
            if collided_sprite:
                collided_sprite.kill()

    def update_scroll_soffset(self):
        if self.player.hitbox_rect.right > self.scroll_offset:
            self.scroll_offset = self.player.hitbox_rect.right
         
    def crf_effect(self):
        self.crt.draw_crt()
        self.crt.create_crt_lines()

    def restart_game(self, level_frames):
        if not self.game_active:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.__init__(level_frames)
                self.game_active = True 
                self.start_time = pygame.time.get_ticks() // 10

    def run(self, dt , level_frames):
        if self.game_active:

            # draw game
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.hitbox_rect.center)
            
            # update game
            self.update_scroll_soffset()
            self.remove_old_sprites()
            self.player_attack()
            self.check_player_death()

            if len(self.platforms) < MIN_PLATFORMS:
                self.generate_new_platforms()

            if len(self.enemies.sprites()) < MIN_ENEMIES:
                self.generate_new_enemies(level_frames)

            self.score.display_score(self.start_time)
            self.crf_effect()
        else:
            restart_surf = self.font.render(f'Press SPACE to restart', False, 'white')
            restart_rect = restart_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            self.display_surface.blit(restart_surf, restart_rect)
            
            self.restart_game(level_frames)
