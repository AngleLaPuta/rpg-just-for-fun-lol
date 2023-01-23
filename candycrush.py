import pygame
import random

# Candy class
class Candy:
    def __init__(self, color):
        self.color = color

# Initialize Pygame
pygame.init()

# Set the size of the game window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the caption of the game window
pygame.display.set_caption("Candy Crush")

# Define the colors of the cand
colors = [(255,0,0), (0,255,0), (0,0,255)]

# Create a 2D grid to represent the game board
board = [[random.choice(colors) for _ in range(5)] for _ in range(5)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked candy
            col = pos[0] // 100
            row = pos[1] // 100
            # Check if a neighboring cell was clicked
            if (row > 0 and pos[1] < (row * 100 + 100)) and (col > 0 and pos[0] < (col * 100 + 100)):
                # Swap the clicked candy with its neighbor
                board[row][col], board[row-1][col] = board[row-1][col], board[row][col]
                # Check for matches
                matches = []
                # Check for horizontal matches
                for r in range(5):
                    for c in range(2):
                        if board[r][c] == board[r][c+1] == board[r][c+2]:
                            matches.append((r,c))
                            matches.append((r,c+1))
                            matches.append((r,c+2))
                # Check for vertical matches
                for r in range(2):
                    for c in range(5):
                        if board[r][c] == board[r+1][c] == board[r+2][c]:
                            matches.append((r,c))
                            matches.append((r+1,c))
                            matches.append((r+2,c))
                # remove the matching cand
               
                for r,c in set(matches):
                    board[r][c] = random.choice(colors)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the game board
    for row in range(5):
        for col in range(5):
            pygame.draw.rect(screen, board[row][col], (col * 100, row * 100, 100, 100))

    # Update the screen
    pygame.display.flip()

# Close the game window
pygame.quit()
