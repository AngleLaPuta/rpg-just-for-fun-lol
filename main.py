from time import sleep
import textwrap
from pytmx import load_pygame
from pathlib import Path
from urllib.parse import urlparse
import sqlite3
import twitter
import math
from copy import deepcopy
import random
from random import choice, randrange, randint
import pygame
import os
import tkinter
import configparser

debug = True

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


class Player:
    def __init__(self):
        self.sprite = pygame.Rect(30, 30, 30, 30)
        self.width = 30
        self.height = 30
        self.x = 300
        self.y = 300
        self.color = (0, 250, 23)
        self.inv=['ball','banana']
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
        x = (size[0]-50*len(self.inv))//2
        y = size[1]-100
        for i in range(0,len(self.inv)):
            tile = pygame.Rect(x,y, 50, 50)
            pygame.draw.rect(screen, (100,100,100), tile)
            pygame.draw.rect(screen, BLACK, tile,2)
            x+=50



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
        global xoffset, yoffset
        speed = 5
        ltile = rtile = dtile = utile = ptile = Tile((self.x + self.width / 2) // tilesize,
                                                     (self.y + self.height / 2) // tilesize)
        for i in range(0, len(tiles)):
            tiles[i].colissions(player.x, player.y)
            if tiles[i].y == ltile.y and tiles[i].x == ptile.x - tilesize:
                if tiles[i].walkable:
                    ltile = tiles[i]
                    #tiles[i].color = RED
                else:
                    ltile = ptile

            if tiles[i].y == rtile.y and tiles[i].x == ptile.x + tilesize:
                if tiles[i].walkable:
                    rtile = tiles[i]
                    #tiles[i].color = GREEN
                else:
                    rtile = ptile

            if tiles[i].x == utile.x and tiles[i].y == ptile.y - tilesize:
                if tiles[i].walkable:
                    utile = tiles[i]
                    #tiles[i].color = YELLOW
                else:
                    utile = ptile
            if tiles[i].x == dtile.x and tiles[i].y == ptile.y + tilesize:
                if tiles[i].walkable:
                    dtile = tiles[i]
                    #tiles[i].color = BLUE
                else:
                    dtile = ptile

            if not (tiles[i] == utile or tiles[i] == dtile or tiles[i] == ltile or tiles[i] == rtile):
                tiles[i].color = None

        for tile in behind:
            if tile.colissions(self.x + self.width / 2, self.y + self.height / 2) and not keys[pygame.K_DOWN] and self.y + self.height > tile.y + tilesize:
                player.y = tile.y

        if 0.2 * size[0] <= self.x + self.width / 2 <= 0.8 * size[0] and 0.2 * size[1] <= self.y + self.height / 2 <= 0.8 * size[1]:
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
                return
        return False


class Sign(Tile):
    def __init__(self, x, y, img, mess, name=None):
        Tile.__init__(self, x, y, img)
        self.x = x
        self.y = y
        self.touched = False
        self.message = mess
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

    def textbox(self, message, width):
        global done
        color = PURPLE
        width = max(int(pygame.font.SysFont('Comic Sans MS', 20).render(message, True, (
            255 - color[0], 255 - color[1], 255 - color[2])).get_width() * 1.1), 400)
        for i in range(0, width):
            rect = pygame.Rect(size[0] / 2 - i / 2, size[1] - 200, i, 100)
            pygame.draw.rect(screen, color, rect, 0)
            pygame.display.flip()
        for i in range(0, len(message)):

            rect = pygame.Rect(size[0] / 2 - width / 2, size[1] - 200, width, 100)
            pygame.draw.rect(screen, color, rect, 0)
            if self.name:
                font = pygame.font.SysFont('Comic Sans MS', 15)
                text = font.render(self.name, True, (255 - color[0], 255 - color[1], 255 - color[2]))
                screen.blit(text, (size[0] / 2 - width / 2, size[1] - 200))
            font = pygame.font.SysFont('Comic Sans MS', 20)
            text = font.render(message[0:i + 1], True, (255 - color[0], 255 - color[1], 255 - color[2]))
            screen.blit(text, (size[0] / 2 - text.get_width() // 2,
                               size[1] - 150 - text.get_height() // 2))
            pygame.display.flip()
            sleep(0.01)
        key = True
        while key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    key = False
                    done = True
                if event.type == pygame.KEYDOWN:
                    key = False


class NPC(Sign):
    def __init__(self, x, y, img, mess, name):
        Sign.__init__(self, x, y, img, mess, name)
        self.walkable = False

class Enemy(NPC):
    def __init__(self, x, y, img, mess, name,func):
        Sign.__init__(self, x, y, img, mess, name)
        self.func = func
    def textbox(self,message,width):
        global name
        Sign.textbox(self,message,width)
        if eval(self.func) == name:
            Sign.textbox(self,'gg',width)
        else:
            Sign.textbox(self,'better luck next time',width)



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
        global screen
        rect = pygame.Rect(self.place[0], self.place[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, rect, 0, 7)
        font = pygame.font.SysFont('Comic Sans MS', 20)
        text = font.render(self.label, True, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]))
        screen.blit(text, (self.place[0] + self.size[0] // 2 - text.get_width() // 2,
                           self.place[1] + self.size[1] // 2 - text.get_height() // 2))


def text(text, x, y, size=20):
    global screen
    font = pygame.font.SysFont('Comic Sans MS', size)
    wrapped_text = textwrap.wrap(text, width=width)
    for i, line in enumerate(wrapped_text):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() * len(wrapped_text) // 2 + i * size))


def load(file):
    global name, fullscreen, pronouns, ft, save, sf, player, xoffset, yoffset, lebel
    sf = file
    save = configparser.ConfigParser()
    save.read(file)

    fullscreen = save.getboolean('META', 'fullscreen')
    name = str(save.get('PLAYER', 'name'))
    pronouns = save.get('PLAYER', 'pronouns')
    pronouns = {'they':pronouns[0],'them':pronouns[1],'their':pronouns[2],'theirs':pronouns[3],'themself':pronouns[4]}
    player.x = save.getint('PLAYER', 'xpos')
    player.y = save.getint('PLAYER', 'ypos')
    lebel = save.getint('PLAYER', 'level')


def backup():
    global name, fullscreen, pronouns, ft, save, sf, player, xoffset, yoffset, lebel
    save.set('PLAYER', 'xpos', str(int(player.x - xoffset)))
    with open(sf, 'w') as savfile:
        save.write(savfile)
    save.set('PLAYER', 'ypos', str(int(player.y - yoffset)))
    with open(sf, 'w') as savfile:
        save.write(savfile)

    save.set('PLAYER', 'level', str(lebel))
    with open(sf, 'w') as savfile:
        save.write(savfile)


def start():
    global size, done

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
        text("INSERT TITLE HERE", size[0] / 2, size[1] * 0.4, 50)
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
    global save
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
                    f.write('[META]\nfullscreen=false\n[PLAYER]\nname=\npronouns=[]\nxpos=10\nypos=10\nlevel=1')
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
    global size, done, pronouns, sf, save

    def off():
        started = True

    started = False
    pronouns = []
    txt = ""
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'poop':
                    pass
                elif event.key == pygame.K_RETURN:
                    pronouns = txt.split('/')
                    if len(pronouns) != 5:
                        pass
                    else:
                        save.set('PLAYER', 'pronouns',
                                 f'[{pronouns[0]},{pronouns[1]},{pronouns[2]},{pronouns[3]},{pronouns[4]}]')
                        with open(sf, 'w') as savfile:
                            save.write(savfile)
                        save.set('META', 'hasplayed', 'true')
                        with open(sf, 'w') as savfile:
                            save.write(savfile)
                        started = True
                elif event.key == pygame.K_BACKSPACE:
                    txt = txt[:-1]
                else:
                    txt += event.unicode
        screen.fill(WHITE)
        text("Please enter your pronouns", size[0] / 2, size[1] * 0.4, 50)
        text("(format 'they/them/their/theirs/themself' please)", size[0] / 2, size[1] * 0.5)

        text(txt, size[0] / 2, size[1] * 0.7)
        pygame.display.flip()
        clock.tick(60)


def pause():
    global size, done

    def off():
        started = True

    sb = button('Continue', BLUE, (size[0] * 0.25, size[1] * 0.75), (100, 50))
    quit = button('Quit', RED, (size[0] * 0.75, size[1] * 0.75), (100, 50))
    save = button('Save', PURPLE, (size[0] * 0.5, size[1] * 0.75), (100, 50))
    started = False
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                backup()
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if sb.click():
                        started = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sb.click():
                    started = True
                if quit.click():
                    backup()
                    done = True
                if save.click():
                    backup()
        screen.fill(WHITE)
        sb.draw()
        quit.draw()
        save.draw()
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
                    player.coins +=points//randint(1,5)
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
        tiled_map = load_pygame(f'level{lebel}.tmx')
    except:
        tiled_map = load_pygame(f'level2.tmx')
    behind = []
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
                tiles.append(Sign(sign.x, sign.y, sign.image,
                                  sign.Message))
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
    if not first:
        for pos in start:
            player.x = pos.x
            player.y = pos.y
    for sign in enemies:
        try:
            tiles.append(Enemy(sign.x, sign.y, sign.image, sign.Message, sign.name,sign.game))
        except:
            pass
    xoffset = 0
    yoffset = 0
    findinfo()

def findinfo():
    global history
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
        "there are bugs in your skin there are bugs in your skin there are bugs in your skin there are bugs in your skin ",
        "make sure to punch a local cop"

    ]
    fun_fact = random.choice(fun_facts)
    history =[]

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
    print(profiles)
    print(player.att)

    visit_count = {}
    for profile in profiles:
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

    # print the sorted dictionary
    for k, v in sorted_visit_count.items():
        # set the background color
        screen.fill((255, 255, 255))

        # display a loading message
        loading_text = "Loading..."
        loading_font = pygame.font.SysFont("Comic Sans MS", 30)
        loading_surface = loading_font.render(loading_text, True, (0, 0, 0))
        loading_rect = loading_surface.get_rect(center=(size[0]//2, 150))
        screen.blit(loading_surface, loading_rect)



        fact_text = f"Fun Fact: {fun_fact}"
        fact_font = pygame.font.SysFont("Comic Sans MS", 20)
        fact_surface = fact_font.render(fact_text, True, (0, 0, 0))
        fact_rect = fact_surface.get_rect(center=(size[0]//2, size[1]-150))
        screen.blit(fact_surface, fact_rect)


        if 'e6' in k or 'furaffinity' in k or 'yiff' in k and 'furry' not in player.att:
            print(f"You're a fuckin furry")
            player.att.append('furry')
            history.append([k,v])
        if 'stackoverflow' in k or 'github' in k and 'programmer' not in player.att:
            print(f"Ahh, a programmer")
            player.att.append('programmer')
            history.append([k, v])
        # update the screen
        pygame.display.update()
    # Close the connection to the database
    print(history)
    player.att = list(set(player.att))
    print(player.att)
    conn.close()
def tetris():
    global screen, clock, size,done, name
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
                   [(0,1),(0,-1),(1,0),(-1,0)]]

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

    def text(text, x, y, size=20):
        global screen
        font = pygame.font.SysFont('Comic Sans MS', size)
        text = font.render(text, True, (255, 255, 255))
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

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
    global size, done, name, pronouns, player, tiles, map, xoffset, yoffset, behind, key, lebel
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
        text(f'Coins:{player.coins}',size[0]-75,50)
        player.invDraw()
        pygame.display.flip()

        clock.tick(60)


player = Player()
start()
fart = randint(0, 3)
play()
