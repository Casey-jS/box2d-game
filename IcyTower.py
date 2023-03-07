import engine 
from game_object import GameObject
import scene
import pygame as pg
import Box2D


class Player(GameObject):

    def __init__(self):
        super().__init__(100, 100, "default.png")
        self.speed = 5

    def update(self):

        print("Player.update() called")

        keys = pg.key.get_pressed()

        if keys[pg.K_a]: self.rect.x -= self.speed
        
        if keys[pg.K_d]: self.rect.x += self.speed
        
        if keys[pg.K_SPACE]: self.rect.y -= self.speed

def main():
    e = engine.Engine("Icy Tower")
    player = Player()

    level = scene.Scene(e)
    e.scene = level

    level.add_object(player)

    e.run()



if __name__ == "__main__":
    main()