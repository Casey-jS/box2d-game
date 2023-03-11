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


def generate_platform(y, world):
    x = random.randint(0, 1024 - PLATFORM_WIDTH)
    p = Platform(x, y, world)
    return p

def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    level = Scene(engine, player)

    platform_heights = [628, 528, 428, 328, 228, 128, 28]
    for h in platform_heights:
        p = generate_platform(h, engine.world)
        level.add_object(p)
    
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()