from engine import Engine
from game_object import GameObject
from scene import Scene
import pygame as pg
import Box2D

pixels_to_meters = 1/100
meters_to_pixels = 100

class Player(GameObject):

    def __init__(self, world, x=768/2, y=400):
        super().__init__(x, y)
        self.speed = 1000
        self.jump_force = -10000
        
        self.body = world.CreateDynamicBody(
            position = (x, y),
            fixedRotation = True
        )
        shape = Box2D.b2PolygonShape(box=(1, 1))
        
        fixture = Box2D.b2FixtureDef(
            shape = shape,
            friction = 0.3,
            restitution = 0.3,
            density = 0.5
        )

        fixture.userData = "player"

        box = self.body.CreateFixture(fixture)

        image: pg.Surface = pg.image.load("default.png").convert_alpha()
        self.image = pg.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        keys = pg.key.get_pressed()
        
        if keys[pg.K_a]: 
            self.body.ApplyForce(Box2D.b2Vec2(-self.speed, 0), self.body.worldCenter, True)
            
        if keys[pg.K_d]: 
            self.body.ApplyForce(Box2D.b2Vec2(self.speed, 0), self.body.worldCenter, True)
              
        if keys[pg.K_SPACE]:
            self.body.ApplyLinearImpulse((0, self.jump_force), self.body.position, True)
        self.x, self.y = self.body.position    
        self.rect.x, self.rect.y = self.x, self.y
        

def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    level = Scene(engine)


    level.add_object(player)
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()