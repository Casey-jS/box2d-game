import pygame
import Box2D
import math

# Define some constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_JUMP_FORCE = 25000
PLAYER_MOVE_SPEED = 10

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Player")

# Define a class for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT

        # Set up Box2D physics for the player
        self.world = Box2D.b2World(gravity=(0, 9.81))
        self.body = self.world.CreateDynamicBody(position=(self.rect.x, self.rect.y))
        self.shape = Box2D.b2PolygonShape(box=(PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2))
        self.fixture = self.body.CreateFixture(shape=self.shape, density=0.5, friction=0.3)

    def update(self, keys):
        # Apply horizontal movement to the player
        if keys[pygame.K_a]:
            self.body.ApplyLinearImpulse((-PLAYER_MOVE_SPEED, 0), self.body.worldCenter, True)
        elif keys[pygame.K_d]:
            self.body.ApplyLinearImpulse((PLAYER_MOVE_SPEED, 0), self.body.worldCenter, True)

        # Jump if the player is on the ground and the jump key is pressed
        if keys[pygame.K_SPACE] and self.rect.bottom == SCREEN_HEIGHT - GROUND_HEIGHT:
            self.body.ApplyLinearImpulse((0, -PLAYER_JUMP_FORCE), self.body.worldCenter, True)

        # Update the Pygame sprite position
        pos = self.body.position
        self.rect.center = (pos.x, SCREEN_HEIGHT - pos.y)

        # Update the Pygame sprite rotation
        angle = -self.body.angle * 180 / math.pi
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

# Define a class for the ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        pass

# Create the player and ground sprites
player = Player()
ground = Ground()

# Create a sprite group and add the player and ground sprites to it
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(ground)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the player and ground sprites
    keys = pygame.key.get_pressed()
    player.update(keys)
    ground.update()

    # Draw the sprites
    screen.fill((255, 255, 255))
    sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Step the Box2D world forward in time
    player.world.Step(1/60, 8, 3)

    # Cap the frame rate
    clock.tick(60)

# Clean up the game
pygame.quit()

   
