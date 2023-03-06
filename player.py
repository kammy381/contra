import pygame
from settings import *
from pygame.math import Vector2 as vector

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((40,80))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft=pos)

        # float pos
        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 400

    def input(self):
        keys = pygame.key.get_pressed()

        #if not self.attacking:
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_SPACE]:
            pass

    def move(self,dt):
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

    def update(self, dt):
        self.input()
        self.move(dt)
