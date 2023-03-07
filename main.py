import pygame
import sys
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from pygame.math import Vector2 as vector
from bullet import Bullet, FireAnimation
from enemy import Enemy


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

        # sky
        self.fg_sky = pygame.image.load('./graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('./graphics/sky/bg_sky.png').convert_alpha()
        self.sky_width = self.bg_sky.get_width()

        self.padding = WINDOW_WIDTH /2
        tmx_map = load_pygame("./data/map.tmx")
        map_width = tmx_map.tilewidth * tmx_map.width + WINDOW_WIDTH
        self.sky_num = int(map_width // self.sky_width)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH /2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

        for x in range(self.sky_num):
            x_pos = -self.padding + (x*self.sky_width)
            self.display_surface.blit(self.bg_sky,(x_pos- self.offset.x/2.5,850- self.offset.y/2.5))
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x/2, 850 - self.offset.y/2))

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        # run setup
        self.setup()

        # bullet graphic load
        self.bullet_surf = pygame.image.load("./graphics/bullet.png").convert_alpha()
        self.fire_surfs = [pygame.image.load('./graphics/fire/0.png').convert_alpha(), pygame.image.load('./graphics/fire/1.png').convert_alpha()]

    def shoot(self, pos, direction, entity):
        Bullet(pos,self.bullet_surf,direction, [self.all_sprites, self.bullet_sprites])
        FireAnimation(entity,self.fire_surfs,direction,self.all_sprites)
    def setup(self):
        tmx_map = load_pygame("./data/map.tmx")

        # collisiontiles
        for x,y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x*64, y*64), surf, [self.all_sprites, self.collision_sprites])
        # tiles
        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x*64, y*64), surf, self.all_sprites, LAYERS[layer])


        # objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, './graphics/player', self.collision_sprites, self.shoot)
            if obj.name == "Enemy":
                Enemy((obj.x, obj.y),"./graphics/enemies/standard",self.all_sprites,self.shoot,self.player,self.collision_sprites)
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == "Platform":
                MovingPlatform((obj.x,obj.y), obj.image, [self.all_sprites,self.collision_sprites, self.platform_sprites])
            else: # border/restraint
                border_rect = pygame.Rect(obj.x, obj.y,obj.width, obj.height)
                self.platform_border_rects.append(border_rect)
    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0: # going up
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y =1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        # obstacles
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle,self.bullet_sprites, True)

        # entities

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            # salmon color fill
            self.display_surface.fill((249, 131, 103))
            self.platform_collisions()
            self.all_sprites.update(dt)
            self.bullet_collisions()

            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()


