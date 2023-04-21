import math
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
        self.canjump = False
        # Set up the player
        self.width = 50
        self.height = 50
        self.x = window_width / 2 - self.width / 2
        self.y = window_height / 2 - self.height / 2
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.5

    def die(self):
        self.canjump = False
        # Set up the player
        self.width = 50
        self.height = 50
        self.x = window_width / 2 - self.width / 2
        self.y = window_height / 2 - self.height / 2
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.5

class player(mover):
    def __init__(self):
        self.canjump = False
        # Set up the player
        self.width = 50
        self.height = 50
        self.x = window_width / 2 - self.width / 2
        self.y = window_height / 2 - self.height / 2
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.5
        # initialize the sword's position and length
        self.sword_x = self.x + self.width / 2
        self.sword_y = self.y + self.height / 2
        self.sword_length = 50

    def move(self):
        # Move the player horizontally
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed = -5
        elif keys[pygame.K_RIGHT]:
            self.x_speed = 5
        else:
            self.x_speed = 0
        if keys[pygame.K_UP] and self.canjump:
            self.y_speed = -15
            self.canjump = False
        elif keys[pygame.K_DOWN]:
            self.y_speed = 15
        self.x += self.x_speed

        # Apply gravity to the player
        self.y_speed += self.gravity
        self.y += self.y_speed

        # Keep the player within the game window
        if self.x < 0:
            self.x = 0
            self.canjump= True
        elif self.x > window_width - self.width:
            self.x = window_width - self.width
            self.canjump=True
        if self.y < 0:
            self.y = 0
        elif self.y > window_height - self.height - 100:
            self.y = window_height - self.height - 100
            self.y_speed = 0
            self.canjump = True

        # Update the sword's position and length
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.sword_x
        dy = mouse_pos[1] - self.sword_y
        angle = math.atan2(dy, dx)
        self.sword_x = self.x  + self.sword_length * math.cos(angle) #+ self.width / 2
        self.sword_y = self.y + self.height / 2 + self.sword_length * math.sin(angle)

    def draw(self):
        # Draw the player and the sword
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), (self.sword_x, self.sword_y, self.sword_length, self.height / 6))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height / 6))
        pygame.draw.rect(window, (0, 0, 255), (self.x, self.y + 5 * self.height / 6, self.width, self.height / 6))
p= player()


class enemy(mover):

    def move(self):
        if randint(0,8)==2:
            self.x_speed = -5
        elif randint(0,8)==2:
            self.x_speed = 5
        if randint(0,100)==2 and self.canjump:
            self.y_speed = -15
            self.canjump = False
        self.x += self.x_speed

        # Apply gravity to the player
        self.y_speed += self.gravity
        self.y += self.y_speed

        # Keep the player within the game window
        if self.x < 0:
            self.x = 0
            self.canjump = True
        elif self.x > window_width - self.width:
            self.x = window_width - self.width
            self.canjump = True
        if self.y < 0:
            self.y = 0
        elif self.y > window_height - self.height - 100:
            self.y = window_height - self.height - 100
            self.y_speed = 0
            self.canjump = True
    def collissions(self):
        if p.x<self.x<p.x+p.width or p.x<self.x+self.width<p.x+p.width:
            #print('baila')
            if self.y<p.y+p.width<self.y+self.height/2:
                self.die()
            if p.y<self.y+self.width<p.y+p.height/2:
                p.die()
        if p.sword_x<self.x<p.sword_x+p.sword_length or p.sword_x<self.x+self.width<p.sword_x+p.sword_length:
            if self.y<p.sword_y+p.width/6<self.y+self.height/2:
                self.die()
    def draw(self):
        pygame.draw.rect(window, (100, 100, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height/6))
        pygame.draw.rect(window, (0, 0, 255), (self.x, self.y + 5*self.height/6, self.width, self.height / 6))




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
    e.collissions()

    # Draw the player
    window.fill((255, 255, 255))
    p.draw()
    e.draw()
    pygame.draw.rect(window, (1, 100, 1), (0, window_height-100, window_width, 100))

    # Update the display
    pygame.display.update()

    # Tick the clock
    clock.tick(60)
