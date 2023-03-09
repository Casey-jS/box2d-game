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
        super().__init__(x=768/2, y=400, world=world, image="default.png", width=PLAYER_SIZE, height=PLAYER_SIZE, type = "dynamic")
        self.speed = 10  # lower speed for smoother momentum
        self.jump_force = -2500
        self.velocity = Box2D.b2Vec2(0, 0)
        self.colliding = False

    def set_colliding(self, colliding):
        self.colliding = colliding
        print("Player.colliding set to " + str(self.colliding))
    def update(self, events):
        self.velocity = self.body.linearVelocity
        
        # update velocity based on keys pressed
        if events[pg.K_a]:
            self.velocity -= Box2D.b2Vec2(self.speed, 0)
        if events[pg.K_d]:
            self.velocity += Box2D.b2Vec2(self.speed, 0)
        
        if events[pg.K_SPACE]:
            self.velocity += Box2D.b2Vec2(0, self.jump_force)

        # apply velocity to body
        self.body.linearVelocity = self.velocity

        if self.x < 0:
            self.velocity.x = abs(self.velocity.x)  # reverse x velocity
        elif self.x > 1024 - PLAYER_SIZE:
            self.velocity.x = -abs(self.velocity.x)

        self.x, self.y = self.body.position
        self.rect.x, self.rect.y = self.x, self.y


class Ground(GameObject):
    def __init__(self, world):
        super().__init__(x = 0, y = 668, world=world, image=None, width = 1024, height = 50, type = "static")  
        print("Rect.x: ", self.rect.x)  
        print("Rect.y: ", self.rect.y)  

        

def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    ground = Ground(engine.world)
    level = Scene(engine, player)

    
    level.add_object(ground)
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()