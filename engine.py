import os
import pygame

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
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.last_time_checked = pygame.time.get_ticks()
        pygame.key.set_repeat(500) # set repeat delay for key presses
        self.paused = False
        self.background = None

    def run(self):
        self.running = True

