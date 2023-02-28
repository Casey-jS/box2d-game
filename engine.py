import os
import pygame as pg
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Engine:

    delta = 0 # time elapsed since last frame
    events = None # current set of events for this frame
    current_scene = None # scene we are currently running

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.running = False
        self.width = width
        self.height = height
        self.pg_init()

    def pg_init(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.last_time_checked = pg.time.get_ticks()
        pg.key.set_repeat(500) # set repeat delay for key presses
        self.paused = False

    def run(self):
        self.running = True
        while self.running:
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


