import textwrap
from time import sleep
from pytmx import load_pygame
from pathlib import Path
from urllib.parse import urlparse
import sqlite3
import locale
import inflect
import math
import ctypes
from copy import deepcopy
import random
from random import choice, randrange, randint
import pygame
import os
import tkinter
import configparser
from translate import Translator

debug = True
gfont = 'Comic Sans MS'

fullscreen = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
pygame.init()
done = False
name = ""
dir_list = os.listdir()
xoffset = 0
yoffset = 0
windll = ctypes.windll.kernel32
print(locale.windows_locale[windll.GetUserDefaultUILanguage()])
lang = locale.windows_locale[windll.GetUserDefaultUILanguage()][:2]

pronouns =['']*5

zaza = pygame.image.load('textures/weed.png')
cookie = pygame.image.load('textures/edible.png')
items = [zaza,cookie]

##TRANSLATIONS AND STUFF
try:
    tr = Translator(to_lang=lang)
    title = tr.translate('INSERT TITLE HERE')
except:
    class trans:
        def translate(self, word):
            return word


    tr = trans()
    title = tr.translate('INSERT TITLE HERE')

sprite = pygame.image.load('sprite.png')

save = configparser.ConfigParser()
sf = 'config.ini'
save.read('config.ini')
fullscreen = False
tilesize = 32
ft = True
for file in dir_list:
    if '.sav' in file:
        ft = False
        break
if fullscreen:
    size = (width, height)
else:
    size = (700, 500)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("the best rpg")
clock = pygame.time.Clock()
lebel = 1
try:
    tiled_map = load_pygame('level1.tmx')
except:
    pass

class TextBox:
    def __init__(self, x, y, width, height, font_size=20, title=""):
        self.rect = pygame.Rect(x-width//2, y, width, height)
        self.font_size = font_size
        self.title = title
        self.text = ""
        self.active = False
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.width = width

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        title_surface = self.font.render(self.title, True, (0, 0, 0))
        screen.blit(title_surface, (self.rect.x, self.rect.y - self.font_size - 5))
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(text_surface, (self.rect.x + self.width //2 - text_surface.get_width()//2, self.rect.y + 5))


class Player:
    def __init__(self):
        self.sprite = pygame.Rect(30, 30, 30, 30)
        self.width = 30
        self.height = 30
        self.x = 500
        self.y = 500
        self.color = (0, 250, 23)
        self.inv = [zaza, cookie]
        self.coins = 0
        self.att = []

    def draw(self):
        global screen, sprite
        sprite = pygame.transform.scale(sprite, (player.width, player.height))
        self.sprite = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(screen, self.color, self.sprite)
        screen.blit(sprite, self.sprite)

    def invDraw(self):
        global screen
        x = (size[0] - 50 * len(self.inv)) // 2
        y = size[1] - 100
        for i in range(0, len(self.inv)):
            tile = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(screen, (100, 100, 100), tile)
            try:
                self.inv[i] = pygame.transform.scale(self.inv[i],(50,50))
                screen.blit(self.inv[i],(x,y))
            except:
                pass
            pygame.draw.rect(screen, BLACK, tile, 2)
            x += 50

    @staticmethod
    def grounded(x, y):
        for i in range(0, len(tiles)):
            if tiles[i].colissions(x, y):
                return True
        return False

    def qstep(self, x, y):
        return self.grounded(self.x + x / 4, self.y + y / 4) and self.grounded(self.x + x / 2,
                                                                               self.y + y / 2) and self.grounded(
            self.x + x * 0.75, self.y + y * 0.75) and self.grounded(self.x + x, self.y + y)

    def move(self, keys):
        global xoffset, yoffset,items
        if randint(0,727)== 69:
            self.inv.append(choice(items))
        speed = 5
        ltile = rtile = dtile = utile = ptile = Tile((self.x + self.width / 2) // tilesize,
                                                     (self.y + self.height / 2) // tilesize)
        for i in range(0, len(tiles)):
            try:
                tiles[i].colissions(player.x, player.y)
                if 0 < tiles[i].x < size[0] and 0 < tiles[i].y < size[1]:
                    if tiles[i].y == ltile.y and tiles[i].x == ptile.x - tilesize:
                        if tiles[i].walkable:
                            ltile = tiles[i]
                            # tiles[i].color = RED
                        else:
                            ltile = ptile
                    if tiles[i].y == rtile.y and tiles[i].x == ptile.x + tilesize:
                        if tiles[i].walkable:
                            rtile = tiles[i]
                            # tiles[i].color = GREEN
                        else:
                            rtile = ptile

                    if tiles[i].x == utile.x and tiles[i].y == ptile.y - tilesize:
                        if tiles[i].walkable:
                            utile = tiles[i]
                            # tiles[i].color = YELLOW
                        else:
                            utile = ptile
                    if tiles[i].x == dtile.x and tiles[i].y == ptile.y + tilesize:
                        if tiles[i].walkable:
                            dtile = tiles[i]
                            # tiles[i].color = BLUE
                        else:
                            dtile = ptile
            except:
                print(f'tile {i} isnt working')

            # if not (tiles[i] == utile or tiles[i] == dtile or tiles[i] == ltile or tiles[i] == rtile):
            # tiles[i].color = None

        for tile in behind:
            if tile.colissions(self.x + self.width / 2, self.y + self.height / 2) and not keys[
                pygame.K_DOWN] and self.y + self.height > tile.y + tilesize:
                player.y = tile.y

        if 0.2 * size[0] <= self.x + self.width / 2 <= 0.8 * size[0] and 0.2 * size[
            1] <= self.y + self.height / 2 <= 0.8 * size[1]:
            if keys[pygame.K_LEFT] and (self.x - speed > ltile.x) and self.grounded(self.x - speed, self.y):
                self.x -= speed
            if keys[pygame.K_RIGHT] and (
                    self.x + self.width + speed < rtile.x + rtile.height) and self.grounded(self.x + speed, self.y):
                self.x += speed
            if keys[pygame.K_UP] and (self.y - speed > utile.y) and self.grounded(self.x, self.y - speed):
                self.y -= speed
            if keys[pygame.K_DOWN] and (
                    self.y + self.height + speed < dtile.y + dtile.height) and self.grounded(self.x, self.y + speed):
                self.y += speed
        elif (self.x + self.width / 2) < 0.2 * size[0]:
            self.x += tilesize * 8 - self.width // 2
            xoffset += tilesize * 7
            for tile in tiles:
                tile.x += tilesize * 7
            for tile in behind:
                tile.x += tilesize * 7
        elif (self.x + self.width / 2) > 0.8 * size[0]:
            self.x -= tilesize * 7 - self.width // 2
            xoffset -= tilesize * 7
            for tile in tiles:
                tile.x -= tilesize * 7
            for tile in behind:
                tile.x -= tilesize * 7
        elif (self.y + self.height / 2) < 0.2 * size[1]:
            self.y += tilesize * 8 - self.height // 2
            yoffset += tilesize * 7
            for tile in tiles:
                tile.y += tilesize * 7
            for tile in behind:
                tile.y += tilesize * 7
        elif (self.y + self.height / 2) > 0.8 * size[1]:
            self.y -= tilesize * 8 - self.height // 2
            yoffset -= tilesize * 7
            for tile in tiles:
                tile.y -= tilesize * 7
            for tile in behind:
                tile.y -= tilesize * 7


class Tile:
    global player

    def __init__(self, x, y, img=None):
        self.width = tilesize
        self.height = tilesize
        self.x = x * self.width
        self.y = y * self.height
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = None
        self.player = player
        self.img = img
        if self.img:
            self.img = pygame.transform.scale(img, (tilesize, tilesize))
        self.walkable = True

    def draw(self):
        if 0 <= self.x <= size[0] and 0 <= self.y <= size[1]:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.img:
                screen.blit(self.img, rect)
            if self.color:
                pygame.draw.rect(screen, self.color, rect, 0)

    def colissions(self, x, y):
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height


class Obstacle(Tile):
    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, img)
        self.walkable = False


class Transport(Tile):
    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, img)
        self.walkable = False
        self.x = x
        self.y = y
        self.width = self.height = tilesize * 2
        self.img = pygame.transform.scale(img, (tilesize * 2, tilesize * 2))
        self.key = ''

    def colissions(self, x, y):
        global lebel, tiled_map
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            self.key = key
            if not self.key == 'z' and not self.key == 'x':
                pass
                # text('Press z or x to continue', size[0] / 2, size[1] - 100, 30)
                pygame.display.flip()
            else:
                lebel += 1
                loadLevel(lebel)
                findinfo()
                return
        return False


class House(Transport):
    def __init__(self, x, y, img, goto):
        Transport.__init__(self, x, y, img)
        self.size = self.height = tilesize
        self.img = pygame.transform.scale(img, (tilesize, tilesize))
        self.goto = goto

    def colissions(self, x, y):
        global lebel, tiled_map
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            self.key = key
            if not self.key == 'z' and not self.key == 'x':
                return True
            else:
                findinfo()
                loadLevel(self.goto)
        return False


class Door(House):
    def __init__(self, x, y, img, goto):
        House.__init__(self, x, y, img, goto)

    def colissions(self, x, y):
        global lebel, tiled_map
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            loadLevel(self.goto)
        return False


class Sign(Tile):
    def __init__(self, x, y, img, mess, name=None):
        Tile.__init__(self, x, y, img)
        self.x = x
        self.y = y
        self.touched = False
        try:
            self.message = tr.translate(format(mess))
        except:
            self.message = format(mess)
        self.name = name

    def colissions(self, x, y):
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            if not self.touched:
                self.textbox(self.message, 400)
                self.touched = True
        else:
            self.touched = False
        return False

    # This function will create a textbox on the screen, meow!
    def textbox(self, message, width):
        global done, gfont
        color = PURPLE
        width = max(int(pygame.font.SysFont(gfont, 20).render('e'*50, True, (
        255 - color[0], 255 - color[1], 255 - color[2])).get_width() * 1.1), 400)
        for i in range(0, width):
            rect = pygame.Rect(size[0] / 2 - i / 2, size[1] - 200, i, 100)
            pygame.draw.rect(screen, color, rect, 0)
            pygame.display.flip()

        lines = textwrap.wrap(message, width=50)
        line_height = 20

        for i, line in enumerate(lines):
            for k in range(len(line)):
                rect = pygame.Rect(size[0] / 2 - width / 2, size[1] - 200, width, 100)
                pygame.draw.rect(screen, color, rect, 0)

                if self.name:
                    font = pygame.font.SysFont(gfont, 15)
                    text = font.render(self.name, True, (255 - color[0], 255 - color[1], 255 - color[2]))
                    screen.blit(text, (size[0] / 2 - width / 2, size[1] - 200))

                font = pygame.font.SysFont(gfont, 20)
                for j in range(0,i):
                    text = font.render(lines[j], True, (255 - color[0], 255 - color[1], 255 - color[2]))
                    screen.blit(text,
                                (size[0] / 2 - text.get_width() // 2,
                                 size[1] - 150 + j * line_height - text.get_height() // 2))

                text = font.render(line[0:k], True, (255 - color[0], 255 - color[1], 255 - color[2]))
                screen.blit(text,
                            (size[0] / 2 - text.get_width() // 2, size[1] - 150 + i * line_height - text.get_height() // 2))
                pygame.display.flip()
                sleep(0.01)
        key = True
        while key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    key = False
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_x:
                        key = False



class NPC(Sign):
    def __init__(self, x, y, img, mess, name):
        Sign.__init__(self, x, y, img, mess, name)
        self.walkable = False

class ConversationalNPC(NPC):
    def __init__(self, x, y, img, dialog, name = 'Nigga'):
        self.dialog = dialog
        self.current_dialog_index = 0
        NPC.__init__(self, x, y, img, '', name)

    def talk(self):
        if self.current_dialog_index < len(self.dialog):
            message = self.dialog[self.current_dialog_index]
            self.textbox(message[self.current_dialog_index], 400)
            self.current_dialog_index += 1

    def collisions(self,x,y):
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            if not self.touched:
                self.talk()
                self.touched = True
                self.current_dialog_index =0
        else:
            self.touched = False
        return False


class Enemy(NPC):
    def __init__(self, x, y, img, mess, name, func):
        Sign.__init__(self, x, y, img, mess, name)
        self.func = func

    def textbox(self, message, width):
        global name
        Sign.textbox(self, message, width)
        if eval(self.func) == name:
            Sign.textbox(self, 'gg', width)
        else:
            Sign.textbox(self, 'better luck next time', width)

class Shopkeeper(NPC):
    def __init__(self, x, y, img,inventory , name = 'Bob'):
        self.inventory = inventory
        NPC.__init__(self, x, y, img, '', name)

    def textbox(self):
        global done, gfont, player
        color = PURPLE
        width = max(int(pygame.font.SysFont(gfont, 20).render('e'*50, True, (
        255 - color[0], 255 - color[1], 255 - color[2])).get_width() * 1.1), 400)

        # create a surface to display the inventory
        inv_surface = pygame.Surface((width, 400))
        inv_surface.fill((255, 255, 255))

        # display the inventory items
        font = pygame.font.SysFont(gfont, 20)
        for i, item in enumerate(self.inventory):
            text = font.render(f"{item.name} ({item.price}$)", True, (0, 0, 0))
            inv_surface.blit(text, (10, i * 30 + 10))

        # display the player's money
        money_text = font.render(f"Money: {player.coins}$", True, (0, 0, 0))
        inv_surface.blit(money_text, (10, 350))

        # draw the inventory surface onto the main screen
        screen.blit(inv_surface, (size[0] / 2 - width / 2, size[1] / 2 - 200))

        # update the display
        pygame.display.flip()

        # handle mouse clicks
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    return
                elif event.type == pygame.MOUSEBUTTONUP:
                    # get the position of the mouse click
                    pos = pygame.mouse.get_pos()

                    # check if the mouse click is inside an inventory item
                    for i, item in enumerate(self.inventory):
                        item_rect = pygame.Rect(size[0] / 2 - width / 2 + 10, size[1] / 2 - 200 + i * 30 + 10, 200, 30)
                        if item_rect.collidepoint(pos):
                            # check if the player has enough money to buy the item
                            if player.coins >= item.price:
                                # subtract the item price from the player's money
                                player.coins -= item.price
                                # add the item to the player's inventory
                                player.inv.append(item)
                                # remove the item from the shop's inventory
                                self.inventory.remove(item)
                                # display a message to confirm the purchase
                                self.textbox(f"You bought {item.name} for {item.price}$!",500)
                                return
                            else:
                                # display a message if the player doesn't have enough money
                                self.textbox("You don't have enough money to buy that!",500)
                                return


    def collisions(self, x, y):
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            if not self.touched:
                self.textbox()
                self.touched = True
        else:
            self.touched = False
        return False



class TransTile(Tile):
    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, img)

    def colissions(self, x, y):
        return False


class Portal(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y)
        self.color = PURPLE

    def colissions(self, x, y):
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            self.teleport(8, 12)

    def teleport(self, x, y):
        x *= tilesize
        y *= tilesize
        player.x = x
        player.y = y


class button:
    def __init__(self, label, color, place, size):
        global tr
        self.tlabel = tr.translate(label)
        self.label = label
        self.color = color
        self.size = size
        self.place = place
        self.place = (self.place[0] - self.size[0] / 2, self.place[1] - self.size[1] / 2)

    def click(self):
        rect = pygame.Rect(self.place[0], self.place[1], self.size[0], self.size[1])
        return rect.collidepoint(pygame.mouse.get_pos())

    def get_label(self):
        return self.label

    def draw(self):
        global screen, gfont
        rect = pygame.Rect(self.place[0], self.place[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, rect, 0, 7)
        font = pygame.font.SysFont(gfont, 20)
        text = font.render(self.tlabel, True, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]))
        screen.blit(text, (self.place[0] + self.size[0] // 2 - text.get_width() // 2,
                           self.place[1] + self.size[1] // 2 - text.get_height() // 2))

def format(text):
    global pronouns,name,tool
    engine = inflect.engine()
    text = text.replace('[they]', pronouns[0])
    text = text.replace('[them]', pronouns[1])
    text = text.replace('[their]', pronouns[2])
    text = text.replace('[theirs]', pronouns[3])
    text = text.replace('[themself]', pronouns[4])
    text = text.replace('[player]', name)
    try:
        text = text.replace('[att]', random.choice(player.att))
        text = text.replace('[atts]', engine.plural(random.choice(player.att)))
    except:
        text = text.replace('[att]', 'person')
        text = text.replace('[atts]', 'people')
    sentences = text.split(".")
    sentences = [s.strip().capitalize() for s in sentences]
    text = ". ".join(sentences) + "."
    return text

def text(text, x, y, size=20):
    global screen, gfont, lang,pronouns, name
    # Define font choices for different languages
    if lang == 'zh':
        gfont = 'Sim Sun'
    elif lang == 'ja':
        gfont = 'Noto Sans JP'
    elif lang == 'ko':
        gfont = 'Nanum Gothic'
    elif lang in ['ar', 'hi']:
        gfont = 'Noto Naskh Arabic'
    else:
        gfont = 'Comic Sans MS'


    text =format(text)

    font = pygame.font.SysFont(gfont, size)
    txt = font.render(text, True, (0, 0, 0))
    wrapped_text = textwrap.wrap(text)
    for i, line in enumerate(wrapped_text):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() * len(wrapped_text) // 2 + i * size))


def load(file):
    global name, fullscreen, pronouns, ft, save, sf, player, xoffset, yoffset, lebel, coins, lang, tr
    sf = file
    save = configparser.ConfigParser()
    save.read(file)

    fullscreen = save.getboolean('META', 'fullscreen')
    name = str(save.get('PLAYER', 'name'))
    pronouns = eval(save.get('PLAYER', 'pronouns'))
    print(pronouns)
    player.x = save.getint('PLAYER', 'xpos')
    player.y = save.getint('PLAYER', 'ypos')
    lebel = save.getint('PLAYER', 'level')
    player.coins = save.getint('PLAYER', 'coins')
    lang = str(save.get('META', 'lang'))
    try:
        tr = Translator(to_lang=lang)
        title = tr.translate('INSERT TITLE HERE')
    except:
        class trans:
            def translate(self, word):
                return word

        tr = trans()


def backup():
    global name, fullscreen, pronouns, ft, save, sf, player, xoffset, yoffset, lebel, coins,lang
    save.set('PLAYER', 'xpos', str(int(player.x - xoffset)))
    with open(sf, 'w') as savfile:
        save.write(savfile)
    save.set('PLAYER', 'ypos', str(int(player.y - yoffset)))
    with open(sf, 'w') as savfile:
        save.write(savfile)
    save.set('PLAYER', 'level', str(lebel))
    with open(sf, 'w') as savfile:
        save.write(savfile)
    save.set('PLAYER', 'coins', str(player.coins))
    with open(sf, 'w') as savfile:
        save.write(savfile)
    save.set('META', 'lang', lang)
    with open(sf, 'w') as savfile:
        save.write(savfile)


def start():
    global size, done, title

    def off():
        started = True

    sb = button('Start', BLUE, (size[0] / 2, size[1] * 0.75), (100, 50))
    started = False
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if sb.click():
                        started = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sb.click():
                    started = True
                    if ft:
                        setName()
                    else:
                        saveFile()
        screen.fill(WHITE)
        sb.draw()
        text(title, size[0] / 2, size[1] * 0.4, 50)
        pygame.display.flip()
        clock.tick(60)


def saveFile():
    global size, done, saveto

    saves = []
    buttons = []

    for file in dir_list:
        if '.sav' in file:
            saves.append(file)
    saves.append("New File")

    for i in range(0, len(saves)):
        buttons.append(button(saves[i].split('.')[0], (randint(0, 128), randint(0, 128), randint(0, 128)),
                              (size[0] / 2, (size[1] / len(saves)) * i + ((size[1] - 100) / (len(saves) * 2))),
                              (size[0] - 100, (size[1] - 200) / len(saves))))

    started = False
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sb in buttons:
                    if sb.click():
                        if sb.label != "New File":
                            return load(sb.label + '.sav')
                        else:
                            return setName()
        screen.fill(WHITE)
        for sb in buttons:
            sb.draw()
        pygame.display.flip()
        clock.tick(60)


def setName():
    global save, sf
    save = configparser.ConfigParser()

    global size, done, name

    def off():
        started = True

    started = False
    name = ""
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'poop':
                    pass
                elif event.key == pygame.K_RETURN:
                    sf = name + '.sav'
                    f = open(sf, 'a')
                    f.write(
                        '[META]\nfullscreen=false\nlang=en\n[PLAYER]\nname=\npronouns=\nxpos=10\nypos=10\nlevel=1\ncoins =0')
                    f.flush()
                    f.close()
                    save.read(sf)
                    save.set('PLAYER', 'name', name)
                    with open(sf, 'w') as savfile:
                        save.write(savfile)
                    started = True
                    return setPronouns()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(WHITE)
        text("What is your name", size[0] / 2, size[1] * 0.4, 50)
        text(name, size[0] / 2, size[1] * 0.7)
        pygame.display.flip()
        clock.tick(60)


def setPronouns():
    global size, done, sf, save

    subject_box = TextBox(size[0] / 2 - 150, size[1] * 0.4, 150, 30, title="Subjective")
    obj_box = TextBox(size[0] / 2 + 150, size[1] * 0.4, 150, 30, title="Objective")
    poss_det_box = TextBox(size[0] / 2 , size[1] * 0.6, 150, 30, title="Possessive Determiner")
    poss_box = TextBox(size[0] / 2 - 150, size[1] * 0.8, 150, 30, title="Possessive")
    reflexive_box = TextBox(size[0] / 2 + 150, size[1] * 0.8, 150, 30, title="Reflexive")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            subject_box.handle_event(event)
            obj_box.handle_event(event)
            poss_det_box.handle_event(event)
            poss_box.handle_event(event)
            reflexive_box.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pronouns = [
                        subject_box.text,
                        obj_box.text,
                        poss_det_box.text,
                        poss_box.text,
                        reflexive_box.text
                    ]
                    if all(pronouns):
                        save.set('PLAYER', 'pronouns', f"['{pronouns[0]}','{pronouns[1]}','{pronouns[2]}','{pronouns[3]}','{pronouns[4]}']")
                        with open(sf, 'w') as savfile:
                            save.write(savfile)
                        save.set('META', 'hasplayed', 'true')
                        with open(sf, 'w') as savfile:
                            save.write(savfile)
                        return
                    else:
                        # Handle case where not all text boxes have text entered
                        pass

        screen.fill(WHITE)
        text("Please enter your pronouns", size[0] / 2, size[1] * 0.2, 50)
        text("(format 'they/them/their/theirs/themself' please)", size[0] / 2, size[1] * 0.3)

        subject_box.draw(screen)
        obj_box.draw(screen)
        poss_det_box.draw(screen)
        poss_box.draw(screen)
        reflexive_box.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def pause():
    global size, done, language, lang, lebel, tr,tool

    # function to turn off the pause screen
    def off():
        started = True

    # uwu, making our buttons for the pause screen
    sb = button('Continue', BLUE, (size[0] * 0.25, size[1] * 0.75), (100, 50))
    quit = button('Quit', RED, (size[0] * 0.75, size[1] * 0.75), (100, 50))
    save = button('Save', PURPLE, (size[0] * 0.5, size[1] * 0.75), (100, 50))
    language_change = button(lang, WHITE, (size[0] * 0.9, size[1] * 0.1), (100, 50))

    # starting the pause screen
    started = False
    while not started and not done:
        for event in pygame.event.get():
            # uwu, quiting the game if the red x is clicked
            if event.type == pygame.QUIT:
                backup()
                done = True
            # uwu, checking if the enter key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if sb.click():
                        started = True
            # uwu, checking if a button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sb.click():
                    loadLevel(lebel)
                    started = True
                # uwu, backing up and quiting the game if the quit button is clicked
                if quit.click():
                    backup()
                    done = True
                # uwu, backing up the game if the save button is clicked
                if save.click():
                    backup()
                # uwu, changing the language if the language change button is clicked
                if language_change.click():
                    language = lang
                    language_list = ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'tl', 'pt', 'ru', 'ar', 'hi', 'ko']
                    current_index = language_list.index(language)
                    language = language_list[(current_index + 1) % len(language_list)]
                    try:
                        print(language)

                        tr = Translator(to_lang=language)
                        lang = language
                        sb = button('Continue', BLUE, (size[0] * 0.25, size[1] * 0.75), (100, 50))
                        quit = button('Quit', RED, (size[0] * 0.75, size[1] * 0.75), (100, 50))
                        save = button('Save', PURPLE, (size[0] * 0.5, size[1] * 0.75), (100, 50))
                        language_change = button(lang, WHITE, (size[0] * 0.9, size[1] * 0.1), (100, 50))

                    except:
                        class trans:
                            def translate(self, word):
                                return word

                        tr = trans()
                        title = tr.translate('INSERT TITLE HERE')
        # uwu, filling the background with white
        screen.fill(WHITE)
        # uwu, drawing our buttons
        sb.draw()
        quit.draw()
        save.draw()
        language_change.draw()
        # uwu, displaying "Paused" on the screen
        text("Paused", size[0] / 2, size[1] * 0.4, 50)
        pygame.display.flip()
        clock.tick(60)


def catch():
    global size, done, name
    start = pygame.time.get_ticks()
    enemy = 'poo monster'
    hard = 10
    balls = [[10, 3]]
    cpuballs = [[size[0] / 2 + 10, 3]]
    square = pygame.Rect(100, size[1] - 100, 50, 50)
    cpu = pygame.Rect(size[0] / 2 + 10, size[1] - 100, 50, 50)
    sb = button('||', GREEN, (50, 50), (50, 50))
    started = False
    points = 0
    cpupoints = 0
    diff = 0

    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sb.click():
                    pause()
        screen.fill(WHITE)
        sb.draw()
        mouse_pos = pygame.mouse.get_pos()
        seconds = 30 - (pygame.time.get_ticks() - start) // 1000
        if seconds <= 0:
            if points == cpupoints:
                seconds += 5
                diff += 5
            else:
                if points > cpupoints:
                    winner = name
                    player.coins += points // randint(1, 5)
                else:
                    winner = enemy
                return winner
        distx = mouse_pos[0] - square.x
        if randint(0, 100 - diff) == 1:
            balls.append([randint(0, size[0] // 2), 0])
            cpuballs.append([randint(size[0] // 2, size[0]), 0])
        if abs(distx) > 1 and mouse_pos[0] <= size[0] / 2:
            square.x += distx
        for ball in balls:
            pygame.draw.circle(screen, GREEN, ball, 20)
            ball[1] += 5
            if square.collidepoint(ball):
                points += 1
                if diff < 95:
                    diff += 1
                balls.remove(ball)
        pygame.draw.rect(screen, BLUE, square)
        text(str(points), size[0] / 4, 20)

        text(f'{name}, use your mouse to get the ball', size[0] / 4, size[1] * 0.4)

        if randint(0, 100 - diff) == 1:
            cpuballs.append([randint(size[0] // 2, size[0]), 0])
            balls.append([randint(0, size[0] // 2), 0])
        try:
            if cpuballs[0][0] - cpu.x > 1 * hard:
                cpu.x += randint(1, 7)
            elif cpuballs[0][0] - cpu.x < -1 * hard:
                cpu.x -= randint(1, 7)
        except:
            pass
        cpu.x = max(size[0] / 2, cpu.x)
        cpu.x = min(size[0], cpu.x)
        for ball in cpuballs:
            pygame.draw.circle(screen, RED, ball, 20)
            ball[1] += 5
            if cpu.collidepoint(ball):
                cpupoints += 1
                if diff < 95:
                    diff += 1
                cpuballs.remove(ball)
            if ball[1] > size[1]:
                cpuballs.remove(ball)
        pygame.draw.rect(screen, GREEN, cpu)
        text(str(cpupoints), size[0] * 0.75, 20)
        text(f'{enemy}, use your mouse to get the ball', size[0] * 0.75, size[1] * 0.4, 10)

        text(str(seconds), size[0] / 2, 20)
        pygame.display.flip()
        clock.tick(60)


def fish():
    global size, done, name
    balls = [[10, size[1]]]
    cpuballs = [[10 + size[0] / 2, size[1]]]
    square = pygame.Rect(size[0] / 2 - 100, 100, 50, 50)
    cpu = pygame.Rect(size[0] - 100, 100, 50, 50)
    sb = button('||', GREEN, (50, 50), (50, 50))
    started = False
    points = 0
    hard = 10
    cpupoints = 0
    enemy = 'poo monster'
    diff = 0
    start = pygame.time.get_ticks()

    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sb.click():
                    pause()

        screen.fill(WHITE)
        sb.draw()
        mx, my = pygame.mouse.get_pos()
        seconds = 30 - (pygame.time.get_ticks() - start) // 1000
        if seconds <= 0:
            if points == cpupoints:
                seconds += 5
                diff += 5
            else:
                if points > cpupoints:
                    winner = name
                    player.coins += points // randint(1, 5)
                else:
                    winner = enemy
                return winner
        distx = mx - square.x
        if randint(0, 50 - diff) == 1:
            balls.append([randint(0, size[0] // 2 - 20), size[1]])
            cpuballs.append([randint(size[0] // 2 + 20, size[0]), size[1]])
        pygame.draw.line(screen, BLACK, (size[0] / 2 - 100, 100), (mx, min(my, 200)))
        water = pygame.Rect((0, 200), size)
        pygame.draw.rect(screen, (0, 128, 128), water)
        for ball in balls:
            pygame.draw.circle(screen, GREEN, ball, 20)
            ball[1] -= diff / 5 + 1
            rect = pygame.Rect(ball, (20, 20))
            if rect.collidepoint(pygame.mouse.get_pos()):
                points += 1
                if diff < 95:
                    diff += 1
                balls.remove(ball)
            elif ball[1] <= 200:
                balls.remove(ball)

        if randint(0, 100 - diff) == 1:
            balls.append([randint(0, size[0] // 2 - 20), size[1]])
            cpuballs.append([randint(size[0] // 2 + 20, size[0]), size[1]])
        try:
            pygame.draw.line(screen, BLACK, (size[0] - 100, 100), (cpuballs[0][0], 200))
        except:
            pass
        for ball in cpuballs:
            pygame.draw.circle(screen, RED, ball, 20)
            ball[1] -= diff / 5 + 1
            if ball[1] <= 200:
                cpuballs.remove(ball)
        if randint(0, 10 * hard) == 7:
            try:
                cpuballs.remove(cpuballs[0])
                cpupoints += 1
            except:
                pass

        pygame.draw.rect(screen, GREEN, square)
        pygame.draw.rect(screen, PURPLE, cpu)
        pygame.draw.line(screen, BLACK, (size[0] / 2, 20), (size[0] / 2, size[1]))
        text("let's go fishing!", size[0] / 2, size[1] * 0.2, 50)
        text(str(points), size[0] / 4, 20)
        text(str(cpupoints), size[0] * 0.75, 20)
        text(str(seconds), size[0] / 2, 20)
        pygame.display.flip()
        clock.tick(60)


def loadLevel(level, first=False):
    global behind, tiles, xoffset, yoffset, player
    try:
        tiled_map = load_pygame(f'level{level}.tmx')
    except:
        tiled_map = load_pygame(f'{level}')
    behind = []
    tiles = []
    tiles = []
    start = tiled_map.get_layer_by_name("Start")
    water = tiled_map.get_layer_by_name("Water")
    land = tiled_map.get_layer_by_name("Land")
    path = tiled_map.get_layer_by_name("Path")
    signs = tiled_map.get_layer_by_name("Sign")
    NPCS = tiled_map.get_layer_by_name("NPC")
    decor = tiled_map.get_layer_by_name("Decor")
    decor2 = tiled_map.get_layer_by_name("Touchable")
    front = tiled_map.get_layer_by_name("Behind")
    leave = tiled_map.get_layer_by_name("Leave")
    enemies = tiled_map.get_layer_by_name("Enemy")
    homes = tiled_map.get_layer_by_name("House")
    doors = tiled_map.get_layer_by_name("Doors")
    try:
        keeps = tiled_map.get_layer_by_name("Shopkeep")
        for sign in keeps:
            try:
                tiles.append(Sign(sign.x, sign.y, sign.image, sign.Message, sign.name))
            except:
                try:
                    tiles.append(Sign(sign.x, sign.y, sign.image, sign.Message))
                except:
                    pass
    except:
        pass

    for x, y, image in water.tiles():
        tiles.append(Obstacle(x, y, image))
    for x, y, image in land.tiles():
        tiles.append(Tile(x, y, image))
    for x, y, image in path.tiles():
        tiles.append(TransTile(x, y, image))
    for sign in signs:
        try:
            tiles.append(Sign(sign.x, sign.y, sign.image, sign.Message, sign.name))
        except:
            try:
                tiles.append(Sign(sign.x, sign.y, sign.image, sign.Message))
            except:
                pass
    for sign in NPCS:
        try:
            tiles.append(NPC(sign.x, sign.y, sign.image, sign.Message, sign.name))
        except:
            pass
    for x, y, image in decor.tiles():
        tiles.append(TransTile(x, y, image))
    for x, y, image in decor2.tiles():
        tiles.append(Obstacle(x, y, image))
    for x, y, image in front.tiles():
        behind.append(Tile(x, y, image))
    for house in leave:
        tiles.append(Transport(house.x, house.y, house.image))
    for house in homes:
        tiles.append(House(house.x, house.y, house.image, house.goto))
    for door in doors:
        tiles.append(Door(door.x, door.y, door.image, door.goto))
    if not first:
        for pos in start:
            player.x = pos.x
            player.y = pos.y
    for sign in enemies:
        try:
            tiles.append(Enemy(sign.x, sign.y, sign.image, sign.Message, sign.name, sign.game))
        except:
            pass
    xoffset = 0
    yoffset = 0


def findinfo():
    global history, tr, lang
    num = 0
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
        "there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin ",
        "make sure to punch a local cop",
        "The tallest mammal in the world is the giraffe, with a height that can reach up to 18 feet.",
        "The largest diamond ever discovered weighed a whopping 3,106 carats!",
        "A group of hedgehogs is called a prickle.",
        "The average person will spend six months of their life waiting for red lights to turn green.",
        "The average person will also spend one year of their life trying to find lost items!",
        "The world's largest pyramid is not in Egypt, but in Mexico!",
        "The world's largest volcano is located in the Pacific Ocean and is named Mauna Loa.",
        "The longest river in the world is the Nile, stretching over 4,000 miles.",
        "The tallest building in the world is the Burj Khalifa in Dubai, standing at over 2,700 feet tall.",
        "The world's largest island is Greenland, with an area of over 840,000 square miles!",
        "The world's largest ocean is the Pacific Ocean, covering over 60 million square miles.",
        "The smallest country in the world is the Vatican City, with a total area of just 0.17 square miles.",
        "The world's largest desert is the Antarctic Desert, covering over 5.5 million square miles!",
        "The world's largest park is the Northeast Greenland National Park, with an area of over 972,000 square miles!",
        "The world's longest cave system is the Mammoth Cave National Park in Kentucky, with over 365 miles of explored passages.",
        "The original design for Mario was actually a carpenter, not a plumber",
        "The first video game to feature a jump button was 1982's Moon Patrol",
        "The original name for the character Pac-Man was Puck-Man, but was changed due to fear of vandalism",
        "The original design for Donkey Kong was actually a Popeye game, but the license was never acquired",
        "In the original version of The Legend of Zelda, the Triforce was actually a triangle made up of hearts, not golden triangles",
        "The game 'Metal Gear Solid' was originally going to be a side-scrolling game, but changed to a full 3D game due to the success of 'Super Mario 64'",
        "In the original version of Sonic the Hedgehog, Sonic could actually spin dash, but it was cut due to hardware limitations",
        "The game 'Tetris' was originally created to be played on a calculator, not a gaming console or computer",
        "The game 'Mortal Kombat' was originally going to feature a type of tag team mode, but was cut due to memory limitations",
        "The original design for the character Mega Man was actually a robot named Rock, but was changed to Mega Man due to copyright issues"

    ]
    fun_fact = random.choice(fun_facts)
    history = []

    user = str(Path.cwd()).split('\\')[2]
    profiles = []
    try:
        path = Path(f'C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
        profiles += [str(f) + '\\places.sqlite' for f in path.iterdir() if f.is_dir()]
    except:
        pass
    try:
        path = Path(f'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data')
        profiles += [str(f) + '\\History' for f in path.iterdir() if f.is_dir()]
    except:
        pass

    visit_count = {}
    for profile in profiles:
        screen.fill((255, 255, 255))
        # display a loading message
        loading_text = "Loading..."
        loading_font = pygame.font.SysFont("Comic Sans MS", 30)
        loading_surface = loading_font.render(loading_text, True, (0, 0, 0))
        loading_rect = loading_surface.get_rect(center=(size[0] // 2, 150))
        screen.blit(loading_surface, loading_rect)

        fact_text = f"Fun Fact: {fun_fact}"
        text(fact_text, size[0] // 2, size[1] - 150)
        # Connect to the "places.sqlite" database
        conn = sqlite3.connect(f'{profile}')
        cursor = conn.cursor()

        # Execute a SQL query to select the URL, title, and visit time from the "moz_places" table

        query = '''
        SELECT * FROM moz_places ORDER BY visit_count ASC
        '''

        try:
            result = cursor.execute(query).fetchall()
            for row in result:
                domain_name = urlparse(row[1]).netloc
                if int(row[4]) > 0:
                    if domain_name in visit_count:
                        visit_count[domain_name] += row[4]
                    else:
                        visit_count[domain_name] = row[4]
        except sqlite3.OperationalError as e:
            pass
    # sort the dictionary by visit count in descending order
    sorted_visit_count = {k: v for k, v in sorted(visit_count.items(), key=lambda item: item[1])}

    num = 0

    loading_text = tr.translate("Loading...")
    fact_text = tr.translate(f"Fun Fact: {fun_fact}")
    # print the sorted dictionary
    for k, v in sorted_visit_count.items():
        # set the background color
        screen.fill((255, 255, 255))

        # display a loading message

        loading_font = pygame.font.SysFont(gfont, 30)
        loading_surface = loading_font.render(loading_text, True, (0, 0, 0))
        loading_rect = loading_surface.get_rect(center=(size[0] // 2, 150))
        screen.blit(loading_surface, loading_rect)

        text(f'{int((num / len(sorted_visit_count)) * 100)}%', size[0] // 2, size[1] // 2)
        num += 1
        text(fact_text, size[0] // 2, size[1] - 150)

        if 'e6' in k or 'furaffinity' in k or 'yiff' in k and 'furry' not in player.att:
            player.att.append('furry')
            history.append([k, v])
        if 'stackoverflow' in k or 'github' in k and 'programmer' not in player.att:
            player.att.append('programmer')
            history.append([k, v])
        # update the screen
        pygame.display.update()

    # Close the connection to the database
    player.att = list(set(player.att))
    if player.att ==[]:
        player.att.append('boring ass person')
    conn.close()


def tetris():
    global screen, clock, size, done, name
    W, H = 8, 13
    TILE = 32
    GAME_RES = W * TILE, H * TILE
    height = 3
    start = pygame.time.get_ticks()
    enemy = "ppp"

    game_sc = pygame.Surface(GAME_RES)
    ai_sc = pygame.Surface(GAME_RES)

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)],
                   [(0, 1), (0, -1), (1, 0), (-1, 0)]]

    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]

    aifigures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    aifigure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    aifield = [[0 for i in range(W)] for j in range(H)]

    anim_count, anim_speed, anim_limit = 0, 30, 2000
    aianim_count, aianim_speed, aianim_limit = 0, 30, 2000
    rot = False

    get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    aifigure, ainext_figure = deepcopy(choice(aifigures)), deepcopy(choice(aifigures))
    color, next_color = get_color(), get_color()
    aicolor, ainext_color = get_color(), get_color()
    ax = 0
    score, lines = 0, 0
    aiscore, ailines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
    aiscores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def check_borders():
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True

    def aicheck_borders():
        try:
            if aifigure[i].x < 0 or aifigure[i].x > W - 1:
                return False
            elif aifigure[i].y > H - 1 or aifield[aifigure[i].y][aifigure[i].x]:
                return False
            return True
        except:
            return False

    def minimax(node, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return node.score
        if type(node) == int:
            return node

        if maximizingPlayer:

            bestValue = -math.inf
            for child in node:
                value = minimax(child, depth - 1, alpha, beta, False)
                bestValue = max(bestValue, value)
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestValue

        else:
            bestValue = math.inf
            for child in node:
                value = minimax(child, depth - 1, alpha, beta, True)
                bestValue = min(bestValue, value)
                beta = min(beta, bestValue)
                if beta <= alpha:
                    break
            return bestValue

    while True:
        screen.fill((15, 15, 15))
        dx, rotate = 0, False
        dy = 1
        screen.blit(game_sc, (20, 20))
        screen.blit(ai_sc, (size[0] // 2 + 20, 20))
        # delay for full lines
        # for i in range(lines):
        # pygame.time.wait(200)
        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
        # move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        # move y
        anim_count += anim_speed * 5
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        # compute score
        score += scores[lines]
        # draw grid
        game_sc.fill((0, 0, 0))
        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
        # draw figure
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)
        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

            # AI VERSION
            # CHECK FOR BEST MOVE
            best_score = -math.inf
            best_ax, best_rot = None, None
            maxcount = 0
            height = H
            he = []
            wi = []
            for i in range(4):
                he.append(aifigure[i].y)
                wi.append(aifigure[i].x)
            for ax in [-1, 1, 0]:
                for rot in [True, False]:
                    for ay in [-1, -2, -3]:
                        for i in range(4):
                            aifigure[i].y = he[i]
                            aifigure[i].x = wi[i]
                        # ATTEMPT MOVE
                        aifigure_old = deepcopy(aifigure)
                        for i in range(4):
                            aifigure[i].x += ax
                            if not aicheck_borders():
                                aifigure = deepcopy(aifigure_old)
                                break
                        # rotate
                        center = aifigure[0]
                        aifigure_old = deepcopy(aifigure)
                        if rot:
                            for i in range(4):
                                x = aifigure[i].y - center.y
                                y = aifigure[i].x - center.x
                                aifigure[i].x = center.x - x
                                aifigure[i].y = center.y + y

                                if not aicheck_borders():
                                    aifigure = deepcopy(aifigure_old)
                                    break
                        # ATTEMPT MOVE DOWN
                        aifigure_old2 = deepcopy(aifigure)
                        for i in range(4):
                            aifigure[i].y += 1
                            if not aicheck_borders():
                                aifigure = deepcopy(aifigure_old2)
                                break

                        # CHECK SCORE
                        line, lines = H - 1, 0
                        holes = []
                        for row in range(H - 1, -1, -1):
                            count = 0
                            missed = W

                            for i in range(W):

                                if aifield[row][i]:
                                    count += 1
                                else:
                                    holes.append(i)
                                aifield[line][i] = aifield[row][i]
                            if count < W:
                                maxcount = max(maxcount, (count ** row) - height ** height)
                                line -= 1
                            else:
                                aianim_speed += 3
                                lines += 1
                        for y in range(H):
                            for x in range(W):
                                if aifield[y][x] != 0:
                                    height = min(height, y)
                        height = H - height
                        # COMPUTE ATTEMPT SCORE
                        empty_space_penalty = 0
                        for i in range(4):
                            if aifield[aifigure[i].y][aifigure[i].x] == 0:
                                empty_space_penalty += 1
                        attempt_score = scores[lines] - height + maxcount - len(holes) - empty_space_penalty

                        # call minimax function to compute the score for the move
                        attempt_score = minimax(aifigure, 4, -math.inf, math.inf, False)

                        # IF BEST SCORE, STORE BEST MOVE
                        if attempt_score > best_score:
                            # if height != H:
                            best_score = attempt_score
                            best_ax = ax
                            best_rot = rot
            for i in range(4):
                aifigure[i].y = he[i]
                aifigure[i].x = wi[i]
            # MOVE
            aifigure_old = deepcopy(aifigure)
            for i in range(4):
                aifigure[i].x += best_ax
                if not aicheck_borders():
                    aifigure = deepcopy(aifigure_old)
                    break
            # rotate
            center = aifigure[0]
            aifigure_old = deepcopy(aifigure)
            if best_rot:
                for i in range(4):
                    x = aifigure[i].y - center.y
                    y = aifigure[i].x - center.x
                    aifigure[i].x = center.x - x
                    aifigure[i].y = center.y + y
                    if not aicheck_borders():
                        aifigure = deepcopy(aifigure_old)
                        break

            # move y
            aianim_count += aianim_speed
            if aianim_count > aianim_limit:
                aianim_count = 0
                aifigure_old = deepcopy(aifigure)
                for i in range(4):
                    aifigure[i].y += 1
                    if not aicheck_borders():
                        for i in range(4):
                            aifield[aifigure_old[i].y][aifigure_old[i].x] = aicolor
                        aifigure, aicolor = ainext_figure, ainext_color
                        ainext_figure, ainext_color = deepcopy(choice(aifigures)), get_color()
                        aianim_limit = 2000
                        break
            # check lines
            line, lines = H - 1, 0
            for row in range(H - 1, -1, -1):
                count = 0
                for i in range(W):
                    if aifield[row][i]:
                        count += 1
                    aifield[line][i] = aifield[row][i]
                if count < W:
                    line -= 1
                else:
                    anim_speed += 3
                    lines += 1
            # compute score
            aiscore += scores[lines]
            # draw grid
            ai_sc.fill((0, 0, 0))
            [pygame.draw.rect(ai_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
            # draw figure
            for i in range(4):
                aifigure_rect.x = aifigure[i].x * TILE
                aifigure_rect.y = aifigure[i].y * TILE
                pygame.draw.rect(ai_sc, aicolor, aifigure_rect)
            # draw field
            for y, raw in enumerate(aifield):
                for x, col in enumerate(raw):
                    if col:
                        aifigure_rect.x, aifigure_rect.y = x * TILE, y * TILE
                        pygame.draw.rect(ai_sc, col, aifigure_rect)

            for i in range(W):
                if aifield[0][i]:
                    aifield = [[0 for i in range(W)] for i in range(H)]
                    anim_count, anim_speed, anim_limit = 0, 30, 2000
                    score += aiscore // 2
                    aiscore -= aiscore // 2
                    for i_rect in grid:
                        pygame.draw.rect(ai_sc, get_color(), i_rect)
                        screen.blit(ai_sc, (size[0] / 2 + 20, 20))
                        pygame.display.flip()
                        clock.tick(200)
            # AI NOW USES BEST MOVE, RATHER THAN RANDOM MOVE
            # ADDED DEEP COPY TO STORE BEST MOVE

        # draw next figure
        # for i in range(4):
        #    figure_rect.x = next_figure[i].x * TILE + 380
        #    figure_rect.y = next_figure[i].y * TILE + 185
        #    pygame.draw.rect(screen, next_color, figure_rect)

        # game over
        for i in range(W):
            if field[0][i]:
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                aiscore += score // 2
                score -= score // 2
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    screen.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
        seconds = 60 - (pygame.time.get_ticks() - start) // 1000
        if seconds <= 0:
            if score == aiscore:
                seconds += 5
            else:
                if score > aiscore:
                    winner = name
                    player.coins += score // randint(1, 5)
                else:
                    winner = enemy
                return winner
        text(str(score), size[0] / 4, 20)
        text(str(aiscore), size[0] * 0.75, 20)
        text(str(seconds), size[0] / 2, 20)
        pygame.display.flip()
        clock.tick(60)


def play():
    global size, done, name, pronouns, player, tiles, map, xoffset, yoffset, behind, key, lebel, tr
    speed = 5
    sb = button('||', GREEN, (50, 50), (50, 50))
    started = False
    portals = [(19, 10)]
    tiles = []
    behind = []
    key = ''
    loadLevel(lebel, True)
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                backup()
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sb.click():
                    pause()
            if event.type == pygame.KEYDOWN:
                key = event.unicode
        keys = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()
        player.move(keys)
        screen.fill((128, 128, 255))
        for i in range(0, len(tiles)):
            tiles[i].draw()
        sb.draw()
        player.draw()
        for i in range(0, len(behind)):
            behind[i].draw()
        text(f'{(player.x - xoffset)},{(player.y - yoffset)}', size[0] / 2, size[1] * 0.2, 50)
        text(f'Coins:{player.coins}', size[0] - 75, 50)
        player.invDraw()
        pygame.display.flip()

        clock.tick(60)


player = Player()
start()
findinfo()
fart = randint(0, 3)
play()
