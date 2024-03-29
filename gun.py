import pygame
from pygame.locals import *
import dataLoad

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, pos, speed, types, imagePath):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = dataLoad.load_image(imagePath, -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        if types == 1:
            self.speed = speed + 2
        elif types == 2:
            self.speed = -1 * (speed + 2)
        self.types = types

    def update(self):
        if self.types == 1:
            if self.rect.midright[0] < 0:
                self.kill()
        elif self.types == 2:
            if self.rect.midleft[0] > 1440:
                self.kill()
        self.move()

    def move(self):
        self.rect.x += self.speed

class DiagonalBullet(Bullet1):
    def __init__(self, pos, speed, types, imagePath, direction):
        super().__init__(pos, speed, types, imagePath)
        self.direction = direction
    def move(self):
        self.rect.x += self.speed
        if self.direction == 1:      #上向き
            self.rect.y += 2
        elif self.direction == 2:    #下向き
            self.rect.y -= 2


class MyBullet(Bullet1):
    def __init__(self, pos, speed, types, imagePath):
        super().__init__(pos, speed, types, imagePath)
        if types == 1:
            self.speed += 4
        elif types == 2:
            self.speed -= 4

class Bomb(Bullet1):
    GRAVITY = 0.3
    def __init__(self, pos, speed, types, imagePath):
        super().__init__(pos, speed, types, imagePath)
        self.speedY = 0.1

    def move(self):
        self.rect.x += self.speed
        self.speedY += self.GRAVITY
        self.rect.y += int(self.speedY)

def gun3Way(pos, speed, types, imagePath):
    bulletA = Bullet1(pos, speed, types, imagePath)
    bulletB = DiagonalBullet(pos, speed, types, imagePath, 1)
    bulletC = DiagonalBullet(pos, speed, types, imagePath, 2)