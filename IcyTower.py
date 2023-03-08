from engine import Engine
from game_object import GameObject
import scene
import pygame as pg
import Box2D


w2b = 1/100
b2w = 100
gravity = Box2D.b2Vec2(0.5, -10.0)
world = Box2D.b2World(gravity,doSleep=False)


class Player(GameObject):

    def __init__(self, world):
        super().__init__(0, 0, world, "default.png")
        self.speed = 5
        self.jump_force = 1000

    def update(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_a]: self.rect.x -= self.speed
        
        if keys[pg.K_d]: self.rect.x += self.speed
        
        if keys[pg.K_SPACE]:
            print("Jumping")
            self.body.ApplyLinearImpulse((0, self.jump_force), self.body.worldCenter, True)
            (self.rect.x, self.rect.y) = self.body.position



class Ground(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.body = world.createStaticBody()

def main():
    engine = Engine("Icy Tower")
    player = Player(world)

    level = scene.Scene(engine)
    engine.set_scene(level)

    level.add_object(player)
    engine.run()

if __name__ == "__main__":
    main()