from engine import Engine
from game_object import GameObject
from scene import Scene
import pygame as pg
import Box2D

pixels_to_meters = 1/100
meters_to_pixels = 100

PLAYER_SIZE = 100

class Player(GameObject):

    def __init__(self, world):
        super().__init__(x=768/2, y=600, world=world, image="default.png", width=PLAYER_SIZE, height=PLAYER_SIZE, type = "dynamic")
        self.speed = .5
        self.jump_force = -1
        self.velocity = Box2D.b2Vec2(0, 0)
        self.is_airborne = True
        print(self.body.mass)
        
    def update(self, events):
        self.velocity = self.body.linearVelocity

        self.check_walls()

        # update velocity based on keys pressed
        if events[pg.K_a]:
            self.velocity -= Box2D.b2Vec2(self.speed, 0)
        if events[pg.K_d]:
            self.velocity += Box2D.b2Vec2(self.speed, 0)
        
        if events[pg.K_SPACE] and not self.is_airborne:
            self.body.ApplyLinearImpulse(Box2D.b2Vec2(0, self.jump_force), self.body.position, True)
            self.is_airborne = True
        
            
        
        # apply velocity to body
        self.body.linearVelocity = self.velocity

        self.x, self.y = self.body.position * meters_to_pixels
        self.rect.x, self.rect.y = self.x, self.y

    def check_walls(self):
        if self.y > 768 - PLAYER_SIZE:
            self.y = 768 - PLAYER_SIZE
            self.body.position = (self.x * pixels_to_meters, self.y * pixels_to_meters)
            self.velocity.y = 0
            self.is_airborne = False
        if self.x < 0:
            self.velocity.x = abs(self.velocity.x)  # reverse x velocity
        elif self.x > 1024 - PLAYER_SIZE:
            self.velocity.x = -abs(self.velocity.x)

class Ground(GameObject):
    def __init__(self, world):
        super().__init__(x = 0, y = 668, world=world, image=None, width = 1024, height = 50, type = "static")  

def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    #ground = Ground(engine.world)
    level = Scene(engine, player)

    
    #level.add_object(ground)
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()