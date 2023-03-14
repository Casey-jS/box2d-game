from engine import Engine
from game_object import GameObject
from scene import Scene
import random
from player import Player

PLATFORM_WIDTH = 200

class IcyTower:

    def __init__(self):
        self.engine = Engine("Icy Tower")
        self.player = Player(self.engine.world)
        self.level = Scene(self.engine, self.player)

        self.player.scene = self.level

        self.generate_platforms()

    def generate_platforms(self):
        prev_position = -100000

        # the height that the platforms will spawn at. start at 628
        start = 628

        # generate platforms
        for i in range(200):

            while True:
                x = random.randint(0, 1024 - PLATFORM_WIDTH)

                # to prevent subsequent platforms from spawning too close
                if abs(prev_position - x) <= 200:
                    continue
                p = Platform(x, start - i*100, self.engine.world)
                prev_position = x
                self.level.add_object(p)
                break

    def start(self):
        self.engine.set_scene(self.level)
        self.engine.run()


class Platform(GameObject):
    def __init__(self, x, y, world):
        super().__init__(x, y, world=world, image="assets/platform.png", width = PLATFORM_WIDTH, height = 40, type = "static")  


def main():

    game = IcyTower()
    game.start()

    

    
    

if __name__ == "__main__":
    main()