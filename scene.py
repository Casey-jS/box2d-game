import pygame as pg

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

class Text:
    def __init__(self, text, x, y, size):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.font = pg.font.Font(None, size)

    def update(self, text):
        self.text = text
        
    def draw(self, win):
        text = self.font.render(self.text, True, (0, 0, 255))
        text_rect = text.get_rect()
        text_rect.x, text_rect.y = self.x, self.y
        win.blit(text, text_rect)
        
class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
        self.camera_offset_y = 0
        self.camera_offset_x = 0
        self.engine = engine
        self.background = pg.Surface((self.engine.width, self.engine.height))
        self.message_timer = 0
        self.message = None
        self.camera_speed = 2
        self.screen_bottom = self.engine.height
        self.text = None

    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        
        self.player.update(events)
        for obj in self.objects:
            obj.update(events)

    def set_background(self, image_path):
        image = pg.image.load(image_path).convert_alpha()
        self.background = pg.transform.scale(image, (self.engine.width, self.engine.height))

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
            
        bg_pos = (0, 0)
        window.blit(self.background, bg_pos)

        # if there is a message to display, check its timer
        if self.message:
            if self.message.timer == 0:
                self.message = None
            else:
                self.message.draw(window)
                self.message.timer -= 1

        if self.text: 
            self.text.draw(window)
        
        # draw the player
        self.player.draw(window, self)

        # draw all other game objects
        for obj in self.objects:
            obj.draw(window, self)
