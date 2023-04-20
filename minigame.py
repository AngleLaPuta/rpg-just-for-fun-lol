from random import randint

import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('2D Movement with Gravity')

# Set up the clock
clock = pygame.time.Clock()

class mover:
    def __init__(self):
        # Set up the player
        self.width = 50
        self.height = 50
        self.x = window_width / 2 - self.width / 2
        self.y = window_height / 2 - self.height / 2
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.5

class player(mover):
    def move(self):
        # Move the player horizontally
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed = -5
        elif keys[pygame.K_RIGHT]:
            self.x_speed = 5
        else:
            self.x_speed = 0
        if keys[pygame.K_UP]:
            self.y_speed = -10
        elif keys[pygame.K_DOWN]:
            self.y_speed = 10
        self.x += self.x_speed

        # Apply gravity to the player
        self.y_speed += self.gravity
        self.y += self.y_speed

        # Keep the player within the game window
        if self.x < 0:
            self.x = 0
        elif self.x > window_width - self.width:
            self.x = window_width - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > window_height - self.height - 100:
            self.y = window_height - self.height - 100
            self.y_speed = 0
    def draw(self):
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height / 6))
        pygame.draw.rect(window, (0, 0, 255), (self.x, self.y + 5 * self.height / 6, self.width, self.height / 6))


class enemy(mover):
    def move(self):
        if randint(0,8)==2:
            self.x_speed = -5
        elif randint(0,8)==2:
            self.x_speed = 5
        if randint(0,100)==2:
            self.y_speed = -10
        self.x += self.x_speed

        # Apply gravity to the player
        self.y_speed += self.gravity
        self.y += self.y_speed

        # Keep the player within the game window
        if self.x < 0:
            self.x = 0
        elif self.x > window_width - self.width:
            self.x = window_width - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > window_height - self.height - 100:
            self.y = window_height - self.height - 100
            self.y_speed = 0
    def draw(self):
        pygame.draw.rect(window, (100, 100, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height/6))
        pygame.draw.rect(window, (0, 0, 255), (self.x, self.y + 5*self.height/6, self.width, self.height / 6))



p= player()
e=enemy()
# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    p.move()
    e.move()

    # Draw the player
    window.fill((255, 255, 255))
    p.draw()
    e.draw()
    pygame.draw.rect(window, (1, 100, 1), (0, window_height-100, window_width, 100))

    # Update the display
    pygame.display.update()

    # Tick the clock
    clock.tick(60)
