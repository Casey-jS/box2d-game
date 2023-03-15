import pygame as pg
import sys

class Message(pg.sprite.Sprite):
    def __init__(self, image_file, x, y, height, width, timer):
        super().__init__()
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = timer
        
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
        self.camera_offset_y = 0
        self.camera_offset_x = 0
        self.engine = engine
        self.background = pg.Surface((1024, 768))
        self.message_timer = 0
        self.message = None
        self.camera_speed = 2
        self.screen_bottom = self.engine.height


    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        
        self.player.update(events)
        for obj in self.objects:
            obj.update(events)

    

        
    def draw(self, window: pg.Surface):

        _, screen_height = window.get_size()

        # if the player is moving downwards, about to move downwards, 
        # or not moving at all, slowly move the camera upwards
        if self.player.body.linearVelocity.y >= -5:
            self.camera_offset_y = self.camera_offset_y + self.camera_speed
            self.screen_bottom -= self.camera_speed

        # otherwise follow the player
        # update the new "bottom" of the screen based on the player's rect position
        else:
            self.camera_offset_y = -self.player.y + screen_height/2
            self.screen_bottom = self.player.rect.bottom + self.engine.height/2
            
        # blit the background image at a fixed position
        bg_pos = (0, 0)
        window.blit(self.background, bg_pos)

        if self.message:
            if self.message.timer == 0:
                self.message = None
            else:
                self.message.draw(window)
                self.message.timer -= 1
        
        # draw the player
        self.player.draw(window, self.engine)

        # draw all other game objects
        for obj in self.objects:
            obj.draw(window, self.engine)

