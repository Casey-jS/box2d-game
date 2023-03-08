import os
import pygame as pg
import sys
from Box2D import b2World

FPS = 60

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Engine:

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.width = width
        self.height = height
        self.delta = 0
        self.paused = False
        self.world = b2World(gravity=(0, -10))
        self.scene = None
        self._init_pygame()


    def run(self):

        while True:
            self._handle_events()
            self._game_loop()
            pg.display.flip()
            self._update_delta()

    def set_scene(self, scene):
        self.scene = scene

    def _init_pygame(self):
        pg.init()
        pg.key.set_repeat(500)
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.last_time_checked = pg.time.get_ticks()


    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def _game_loop(self):
        if not self.paused:
            if self.scene:
                self.scene.update()
            self.screen.fill((255, 255, 255))
            if self.scene:
                self.scene.draw(self.screen)

    def _update_delta(self):
        now = pg.time.get_ticks()
        self.delta = now - self.last_time_checked
        self.last_time_checked = now

    @property
    def delta_seconds(self):
        return self.delta / 1000.0

    @property
    def events(self):
        return pg.event.get()
