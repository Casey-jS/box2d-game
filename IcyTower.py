from engine import Engine
from game_object import GameObject
from scene import Scene
import pygame as pg
import Box2D
import random
from player import Player

PLATFORM_WIDTH = 300

class Platform(GameObject):
    def __init__(self, x, y, world):
        super().__init__(x, y, world=world, image="assets/platform.png", width = PLATFORM_WIDTH, height = 40, type = "static")  


def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    level = Scene(engine, player)

    prev_position = -100000

    # the height that the platforms will spawn at. start at 628
    start = 628

    # generate platforms
    for i in range(30):

        while True:
            x = random.randint(0, 1024 - PLATFORM_WIDTH)

            # to prevent subsequent platforms from spawning too close
            if abs(prev_position - x) <= 200:
                continue
            p = Platform(x, start - i*200, engine.world)
            prev_position = x
            level.add_object(p)
            break

    
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()