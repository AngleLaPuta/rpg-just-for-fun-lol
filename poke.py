import random
import pygame

# initialize the game window
pygame.init()
screen = pygame.display.set_mode((800, 600))

# list of all possible pokemon names
pokemon_names = ["Sparky", "Flameon", "Blubber", "Leafy", "Mystic", "Mystique"]

# list of all possible moves and their damage level
moves = [("Thunder Strike", 50), ("Flame Wave", 60), ("Water Surge", 40), ("Vine Smack", 30), ("Shadow Punch", 70), ("Swift Strike", 50)]

def text(text, x, y, size=20):
    global screen
    font = pygame.font.SysFont('Comic Sans MS', size)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

# class to represent each pokemon
class Pokemon:
    def __init__(self, name, health, attack, defense, move):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.move = move
        
    def take_damage(self, damage):
        self.health -= damage
        
    def use_move(self, other_pokemon):
        damage = self.attack - other_pokemon.defense
        if damage < 0:
            damage = 0
        other_pokemon.take_damage(damage)
        
# function to randomly generate a pokemon
def generate_pokemon():
    name = random.choice(pokemon_names)
    health = random.randint(50, 100)
    attack = random.randint(20, 80)
    defense = random.randint(10, 30)
    move = [random.choice(moves),random.choice(moves),random.choice(moves)]
    return Pokemon(name, health, attack, defense, move)

# initialize the two pokemon
pokemon1 = generate_pokemon()
pokemon2 = generate_pokemon()

# function to render text
def text(text, x, y, size=20):
    font = pygame.font.SysFont('Comic Sans MS', size)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

# main game loop
running = True
turn = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # clear the screen
    screen.fill((255, 255, 255))
    
    # draw pokemon 1
    pygame.draw.circle(screen, (255, 0, 0), (100, 300), 50)
    text(pokemon1.name, 50, 300, 30)
    
    # draw pokemon 2
    pygame.draw.circle(screen, (0, 255, 0), (700, 300), 50)
    text(pokemon2.name, 750, 300, 30)
    
        # handle player's turn
    if turn == 1:
        # display the mov
        # e options
        text(f"{pokemon1.name}'s turn", 400, 300)
        text(f"1. {pokemon1.move[0]}", 300, 350)
        text(f"2. {pokemon1.move[1]}", 300, 550)
        text(f"3. {pokemon1.move[2]}", 700, 750)
        
        # handle mouse clicks on the moves
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 380 and 350 <= mouse_pos[1] <= 380:
                    move = pokemon1.move[0]
                    pokemon1.use_move(pokemon2)
                    turn = 2
                elif 500 <= mouse_pos[0] <= 580 and 350 <= mouse_pos[1] <= 380:
                    move = pokemon1.move[1]
                    pokemon1.use_move(pokemon2)
                    turn = 2
                elif 700 <= mouse_pos[0] <= 780 and 350 <= mouse_pos[1] <= 380:
                    move = pokemon1.move[2]
                    pokemon1.use_move(pokemon2)
                    turn = 2

    
    # display the results of the player's move
    if turn == 2:
        text(f"{pokemon1.name} used {move[0]}!", 400, 400)
        text(f"{pokemon2.name} took {move[1]} damage!", 400, 450)
        text("Press any key to continue...", 400, 500)
        keys = pygame.key.get_pressed()
        if any(keys):
            turn = 3
    
    # display the results of the opponent's move
    if turn == 3:
        opponent_move = random.choice(pokemon2.move)
        pokemon2.use_move(pokemon1)
        text(f"{pokemon2.name} used {opponent_move[0]}!", 400, 400)
        text(f"{pokemon1.name} took {opponent_move[1]} damage!", 400, 450)
        text("Press any key to continue...", 400, 500)
        keys = pygame.key.get_pressed()
        if any(keys):
            turn = 1
    
    # display the health of each pokemon
    text(f"{pokemon1.name}'s health: {pokemon1.health}", 200, 100)
    text(f"{pokemon2.name}'s health: {pokemon2.health}", 600, 100)
    
    # check if either pokemon has fainted (health <= 0)
    if pokemon1.health <= 0:
        text(f"{pokemon1.name} has fainted!", 400, 200)
        text("Press any key to quit...", 400, 250)
        keys = pygame.key.get_pressed()
        if any(keys):
            running = False
    elif pokemon2.health <= 0:
        text(f"{pokemon2.name} has fainted!", 400, 200)
        text("Press any key to quit...", 400, 250)
        keys = pygame.key.get_pressed()
        if any(keys):
            running = False
    
    # update the screen
    pygame.display.update()

# quit pygame
pygame.quit()
