import pygame as pg

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

