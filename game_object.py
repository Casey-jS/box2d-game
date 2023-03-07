import pygame as pg

from abc import abstractmethod

'''
GameObject
- Position (x, y)
- Image
- Rectangle
'''

class GameObject(pg.sprite.Sprite):

    def __init__(self, x, y, image="default.png"):
        super().__init__()
        self.x = x
        self.y = y

        self.image: pg.Surface = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 5

    
    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self):
        pass



