import pygame

# initialize the game engine
pygame.init()

# set the window size
window_size = (450, 450)

# create the window
screen = pygame.display.set_mode(window_size)

# set the title of the window
pygame.display.set_caption("Tic Tac Toe")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# dimensions of each cell
cell_size = 150

# number of rows and columns
ROWS = 3
COLS = 3

# initialize the board
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

# player's turn
turn = "X"

# game over flag
game_over = False

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 3)
            if board[row][col] == "X":
                draw_x(row, col)
            elif board[row][col] == "O":
                draw_o(row, col)

def draw_x(row, col):
    x1 = col * cell_size + 10
    y1 = row * cell_size + 10
    x2 = x1 + cell_size - 20
    y2 = y1 + cell_size - 20
    pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 5)
    pygame.draw.line(screen, BLACK, (x2, y1), (x1, y2), 5)

def draw_o(row, col):
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2
    pygame.draw.circle(screen, BLACK, (x, y), cell_size // 3, 3)

def get_cell(mouse_pos):
    row = mouse_pos[1] // cell_size
    col = mouse_pos[0] // cell_size
    return row, col

def ai_move():
    global turn
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is None:
                board[row][col] = turn
                if check_win(turn):
                    return
                turn = "X" if turn == "O" else "O"
                return

def check_win(player):
    for row in range(ROWS):
        if all(board[row][col] == player for col in range(COLS)):
            return True
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return True
    if all(board[i][i] == player for i in range(ROWS)):
        return True
    if all(board[i][    ROWS - i - 1] == player for i in range(ROWS)):
        return True
    return False

while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            row, col = get_cell(pygame.mouse.get_pos())
            if board[row][col] is None:
                board[row][col] = turn
                turn = "O" if turn == "X" else "X"
                if check_win(turn):
                    game_over = True

    # clear the screen
    screen.fill((255, 255, 255))

    # draw the board
    draw_board()

    # make the AI move if it's its turn
    if turn == "O" and not game_over:
        ai_move()

    # check if game is over
    if check_win("X") or check_win("O"):
        game_over = True
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # update the screen
    pygame.display.update()

