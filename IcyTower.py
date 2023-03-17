from engine import Engine
from game_object import GameObject
from scene import Scene, Text
import random
from player import Player
import sys
import pygame as pg
from pygame import mixer, Rect, display, font

PLATFORM_WIDTH = 150

class IcyTower:

    def __init__(self):
        self.engine = Engine("Icy Tower")
        self.player = Player(self.engine.world, self)
        self.level = Scene(self.engine, self.player)

        self.player.scene = self.level
        self.win = False

        self.generate_platforms()
        self.score = 0
        self.score_text = Text("Score: " + str(int(self.score)), 20, 20, 40)
        self.level.text = self.score_text
        mixer.init()
        mixer.music.load("assets/song.mp3")
        mixer.music.play()
    
        self.level.set_background("assets/ice-background.png")

    def set_score(self, val):
        self.score = val

    def generate_platforms(self):
        prev_position = -100000

        # the height that the platforms will spawn at. start at 628
        start = 628

        p = Platform(50, start, self.engine.world)
        self.level.add_object(p)

        # generate platforms
        for i in range(1, 100):
            while True:
                # randomly choose an x coordinate for the platform
                x = random.randint(0, self.engine.width - PLATFORM_WIDTH)

                # to prevent subsequent platforms from spawning too close
                if abs(prev_position - x) <= 200:
                    continue # try again
                p = Platform(x, start - i*100, self.engine.world)
                prev_position = x
                self.level.add_object(p)
                break

        # the height that the second level starts at
        # distance between platforms * number of platforms + initial height
        second_level_start = 628 - (100 * 100) 

        for i in range(100):
            while True:
                x = random.randint(0, self.engine.width - PLATFORM_WIDTH)

                # to prevent subsequent platforms from spawning too close
                if abs(prev_position - x) <= 200:
                    continue
                p = Platform(x, second_level_start - i*100, self.engine.world)
                p.set_platform("assets/platform2.png")
                prev_position = x
                self.level.add_object(p)
                break

    def start(self):
        self.engine.set_scene(self.level)
        self.engine.run()
        self.game_over()

    def game_over(self):
        pg.init()
        win = display.set_mode((400, 600))
        pg.display.set_caption("Game Over")
        win.fill((0, 0, 0))
        font = pg.font.Font(None, 40)

        centerx = win.get_rect().centerx
        centery = win.get_rect().centery

        go_text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        score_rect = score_text.get_rect(centerx = centerx, centery = centery + 100)

        if self.win:
            win_text = font.render("You Won!", True, (0, 255, 0))
            win_rect = win_text.get_rect(centerx = centerx, centery = win.get_rect().top + 100)
            win.blit(win_text, win_rect)
        go_rect = go_text.get_rect()
        go_rect.centerx = win.get_rect().centerx
        go_rect.centery = win.get_rect().top + 50
        win.blit(go_text, go_rect)
        win.blit(score_text, score_rect)

        exit_button = Rect(0, 200, 100, 50)
        exit_button.centerx = win.get_rect().centerx

        new_game_button = Rect(0, 300, 140, 60)
        new_game_button.centerx = win.get_rect().centerx

        exit_text = font.render("Exit", True, (0, 0, 0))
        new_game_text = font.render("New Game", True, (0, 0, 0))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        pg.quit()
                        sys.exit() # exit both windows
                    elif new_game_button.collidepoint(event.pos):
                        pg.quit()
                        game = IcyTower()
                        game.start()
            
            # draw buttons and text
            pg.draw.rect(win, (255, 255, 255), exit_button)
            pg.draw.rect(win, (255, 255, 255), new_game_button)
            exit_text_rect = exit_text.get_rect()
            exit_text_rect.center = (exit_button.x + exit_button.width // 2, exit_button.y + exit_button.height // 2)
            win.blit(exit_text, exit_text_rect)   
            new_game_text_rect = new_game_text.get_rect()
            new_game_text_rect.center = (new_game_button.x + new_game_button.width // 2, new_game_button.y + new_game_button.height // 2)
            win.blit(new_game_text, new_game_text_rect)
            pg.display.update()

class Platform(GameObject):
    def __init__(self, x, y, world):
        super().__init__(x, y, world=world, image="assets/platform.png", width = PLATFORM_WIDTH, height = 40, type = "static")  
    
    def set_platform(self, image_path):
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (PLATFORM_WIDTH, 40))

def main():
    game = IcyTower()
    game.start()

if __name__ == "__main__":
    main()