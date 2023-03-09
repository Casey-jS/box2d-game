import pygame as pg
import Box2D

from abc import abstractmethod

'''
GameObject
- Position (x, y)
- Image
- Rectangle
- Speed
'''

class GameObject(pg.sprite.Sprite):

    def __init__(self, x, y, speed=10):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed



    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self):
        pass
