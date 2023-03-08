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

    def __init__(self, x, y, world, image="default.png", speed=10):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed

        self.image: pg.Surface = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = (self.x, self.y)
        self.body = world.CreateBody(body_def)

        shape = Box2D.b2PolygonShape()
        shape.SetAsBox(self.rect.width * 0.5, self.rect.height * 0.5)
        fixture_def = Box2D.b2FixtureDef(shape=shape, density=1, friction=0.3)
        self.body.CreateFixture(fixture_def)

    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self):
        pass
