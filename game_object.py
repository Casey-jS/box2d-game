import pygame as pg
from Box2D import b2PolygonShape

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
        
        image_temp = pg.image.load(image).convert_alpha()
        self.image = pg.transform.scale(image_temp, (width, height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.world = world

        if type == "dynamic":
            self.body = self.world.CreateDynamicBody(position=(self.rect.x * pixels_to_meters, self.rect.y * pixels_to_meters), fixedRotation=True)
        else:
            self.body = self.world.CreateStaticBody(position=(self.rect.x, self.rect.y), fixedRotation=True)
        self.shape = b2PolygonShape()
        self.shape.SetAsBox(self.rect.width / 2 * pixels_to_meters, self.rect.height / 2 * pixels_to_meters)
        
        self.fixture = self.body.CreateFixture(shape=self.shape, density=.3, friction=0.3, restitution=0.5)
    
    



    def draw(self, window, engine):

        # draw everything based on camera offset
        image_x = self.rect.x + engine.scene.camera_offset[0]
        image_y = self.rect.y + engine.scene.camera_offset[1]
        window.blit(self.image, (image_x, image_y))

    @abstractmethod
    def update(self, events):
        pass
