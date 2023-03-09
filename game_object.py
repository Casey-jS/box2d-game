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

meters_to_pixels = 100
pixels_to_meters = 1/100

class GameObject(pg.sprite.Sprite):

    def __init__(self, x, y, world, image, width, height, type):
        super().__init__()
        self.x = x
        self.y = y
        if not image:
            image_temp = pg.Surface((width, height))
            image_temp.fill((0, 0, 0))
            self.image = image_temp
        else:
            image_temp = pg.image.load(image).convert_alpha()
            self.image = pg.transform.scale(image_temp, (width, height))
        self.rect = self.image.get_rect() # rect is 100px by 100px
        self.rect.x = x
        self.rect.y = y

        self.world = world

        if type == "dynamic":
            self.body = self.world.CreateDynamicBody(position=(self.rect.x, self.rect.y), fixedRotation=True)
        else:
            self.body = self.world.CreateStaticBody(position=(self.rect.x, self.rect.y), fixedRotation=True)
        print(self.body.mass)
        self.shape = Box2D.b2PolygonShape()
        self.shape.SetAsBox(self.rect.width / 2 * pixels_to_meters, self.rect.height / 2 * pixels_to_meters)
        
        self.fixture = self.body.CreateFixture(shape=self.shape, density=.5, friction=0.3, restitution=0.5)
    
    



    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self, events):
        pass
