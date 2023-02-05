import pygame
import time
import random

# initialize pygame
pygame.init()

# set the screen size and title
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Loading Screen")

# set the background color
screen.fill((255, 255, 255))

# display a loading message
loading_text = "Loading..."
loading_font = pygame.font.SysFont("Comic Sans MS", 30)
loading_surface = loading_font.render(loading_text, True, (0, 0, 0))
loading_rect = loading_surface.get_rect(center=(250, 250))
screen.blit(loading_surface, loading_rect)

# display a fun fact
fun_facts = [
    "The average person spends 6 months of their life waiting on a red light to turn green.",
    "Femboys are amazing.",
    "The shortest war in history was between Britain and Zanzibar on 27 August 1896.",
    "The human nose can detect over 1 trillion different scents.",
    "The world's largest snowflake was 15 inches wide and 8 inches thick.",
    "A human head can survive around 10 seconds separated from the body.",
    "auto von Bismarck predicted the resignation Kaiser Wilhelm II, his prediction was 2 month off",
    "every second you're not running, i'm only getting closer",
    "You do not want to fight 15 koalas",
    "According to Marc Laidlaw in Half-Life 2: Raising the Bar, Half-Life 1 takes place in 2003 and Half-Life 2 takes place 20 years after!",
    "To improve at the game, simply stop losing",
    "this is a loading screen",
    "press Alt + F4 for help!",
    "Did you know that a school of jellyfish is called a smack?",
    "Rabbits are cats but with the autism as the exponent instead of an add on",
    "press Alt + F4 to activate the debug menu!",
    "Every 60 seconds in Africa, a minute passes.",
    "The fog is coming",
    "they are coming for you. run",
    "there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin ",
    "make sure to punch a local cop"


    
]
fun_fact = random.choice(fun_facts)
fact_text = f"Fun Fact: {fun_fact}"
fact_font = pygame.font.SysFont("Comic Sans MS", 20)
fact_surface = fact_font.render(fact_text, True, (0, 0, 0))
fact_rect = fact_surface.get_rect(center=(250, 450))
screen.blit(fact_surface, fact_rect)

# update the screen
pygame.display.update()

# wait for 2-3 seconds
time.sleep(2 + random.random())

# quit pygame
pygame.quit()