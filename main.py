import math
from time import sleep
import asyncio
import pytmx
from pytmx import load_pygame
from random import randint
import twitter

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
path = "C://Users//wwsuser1//PycharmProjects//the best fucking rpg youve ever seen watch me"
dir_list = os.listdir(path)
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
tiled_map = load_pygame('level1.tmx')


class Player:
    def __init__(self):
        self.sprite = pygame.Rect(30, 30, 30, 30)
        self.width = 30
        self.height = 30
        self.x = 300
        self.y = 300
        self.color = (0, 250, 23)

    def draw(self):
        global screen, sprite
        sprite = pygame.transform.scale(sprite, (player.width, player.height))
        self.sprite = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(screen, self.color, self.sprite)
        screen.blit(sprite, self.sprite)

    def grounded(self, x, y):
        for i in range(0, len(tiles)):
            if (tiles[i].colissions(x, y)):
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
                    tiles[i].color = RED
                else:
                    ltile = ptile

            if tiles[i].y == rtile.y and tiles[i].x == ptile.x + tilesize:
                if tiles[i].walkable:
                    rtile = tiles[i]
                    tiles[i].color = GREEN
                else:
                    rtile = ptile

            if tiles[i].x == utile.x and tiles[i].y == ptile.y - tilesize:
                if tiles[i].walkable:
                    utile = tiles[i]
                    tiles[i].color = YELLOW
                else:
                    utile = ptile
            if tiles[i].x == dtile.x and tiles[i].y == ptile.y + tilesize:
                if tiles[i].walkable:
                    dtile = tiles[i]
                    tiles[i].color = BLUE
                else:
                    dtile = ptile

            if not (tiles[i] == utile or tiles[i] == dtile or tiles[i] == ltile or tiles[i] == rtile):
                tiles[i].color = None

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
            self.x += (tilesize) * 8 - self.width // 2
            xoffset += tilesize * 7
            for tile in tiles:
                tile.x += tilesize * 7
            for tile in behind:
                tile.x += tilesize * 7
        elif (self.x + self.width / 2) > 0.8 * size[0]:
            self.x -= (tilesize) * 7 - self.width // 2
            xoffset -= tilesize * 7
            for tile in tiles:
                tile.x -= tilesize * 7
            for tile in behind:
                tile.x -= tilesize * 7
        elif (self.y + self.height / 2) < 0.2 * size[1]:
            self.y += (tilesize) * 8 - self.height // 2
            yoffset += tilesize * 7
            for tile in tiles:
                tile.y += tilesize * 7
            for tile in behind:
                tile.y += tilesize * 7
        elif (self.y + self.height / 2) > 0.8 * size[1]:
            self.y -= (tilesize) * 8 - self.height // 2
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
        if 0 <= self.x <= size[0]  and 0 <= self.y <= size[1] :
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
        global lebel, tiled_map, key
        width = player.width
        height = player.height
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if x + width >= self.x and y + height >= self.y and x <= self.x + self.width and y <= self.y + self.height:
            self.key = key
            if not self.key == 'z' and not self.key == 'x':
                pass
                #text('Press z or x to continue', size[0] / 2, size[1] - 100, 30)
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
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def load(file):
    global name, fullscreen, pronouns, ft, save, sf, player, xoffset, yoffset,lebel
    sf = file
    save = configparser.ConfigParser()
    save.read(file)

    fullscreen = save.getboolean('META', 'fullscreen')
    name = str(save.get('PLAYER', 'name'))
    pronouns = save.get('PLAYER', 'pronouns')
    player.x = save.getint('PLAYER', 'xpos')
    player.y = save.getint('PLAYER', 'ypos')
    lebel = save.getint('PLAYER', 'level')


def backup():
    global name, fullscreen, pronouns, ft, save, sf, player, xoffset, yoffset,lebel
    save.set('PLAYER', 'xpos', str(int(player.x - xoffset)))
    with open(sf, 'w') as savfile:
        save.write(savfile)
    save.set('PLAYER', 'ypos', str(int(player.y - yoffset)))
    with open(sf, 'w') as savfile:
        save.write(savfile)

    save.set('PLAYER', 'level', str(lebel))
    with open(sf, 'w') as savfile:
        save.write(savfile)


async def start():
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
                print(pygame.mouse.get_pos())
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
        await asyncio.sleep(0)
        clock.tick(60)


async def saveFile():
    global size, done, saveto

    saves = []
    buttons = []

    for file in dir_list:
        if '.sav' in file:
            saves.append(file)
    saves.append("New File")

    for i in range(0, len(saves)):
        buttons.append(button(saves[i].split('.')[0], (randint(0, 128), randint(0, 128), randint(0, 128)),
                              (size[0] / 2, (size[1] / len(saves)) * (i) + ((size[1] - 100) / (len(saves) * 2))),
                              (size[0] - 100, (size[1] - 200) / len(saves))))

    started = False
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                for sb in buttons:
                    if sb.click():
                        if sb.label != "New File":
                            return load(sb.label + '.sav')
                        else:
                            return setName()
                        started = True
                        break
        screen.fill(WHITE)
        for sb in buttons:
            sb.draw()
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)


async def setName():
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
                    f.write('[META]\nfullscreen=false\n[PLAYER]\nname=\npronouns=[]\nxpos=10\nypos=10')
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
        await asyncio.sleep(0)
        clock.tick(60)


async def setPronouns():
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
                        print("Nigga you need use the right amount of pronouns fucking dumbass")
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
        await asyncio.sleep(0)
        clock.tick(60)


async def pause():
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
                print(pygame.mouse.get_pos())
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
        await asyncio.sleep(0)
        clock.tick(60)


async def catch():
    global size, done, name
    start = pygame.time.get_ticks()
    enemy = 'poo monster'
    hard = 10
    balls = [[10, 3]]
    cpuballs = [[size[0]/2+10, 3]]
    square = pygame.Rect(100, size[1] - 100, 50, 50)
    cpu = pygame.Rect(size[0]/2+10, size[1] - 100, 50, 50)
    sb = button('||', GREEN, (50, 50), (50, 50))
    started = False
    points = 0
    cpupoints=0
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
            if points==cpupoints:
                seconds+=5
                diff+=5
            else:
                if points>cpupoints:
                    winner = name
                else:
                    winner = enemy
                print('The winner is '+winner)
                return winner
                started = True
        distx = mouse_pos[0]- square.x
        if randint(0, 100 - diff) == 1:
            balls.append([randint(0, size[0]/2), 0])
            cpuballs.append([randint(size[0] / 2, size[0]), 0])
        if abs(distx) > 1 and mouse_pos[0]<=size[0]/2:
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
        text(str(points), size[0]/4, 20)

        text(f'{name}, use your mouse to get the ball', size[0] / 4, size[1] * 0.4)

        if randint(0, 100 - diff) == 1:
            cpuballs.append([randint(size[0]/2, size[0]), 0])
            balls.append([randint(0, size[0] / 2), 0])
        try:
            if cpuballs[0][0]-cpu.x>1*hard:
                cpu.x+= randint(1,7)
            elif cpuballs[0][0]-cpu.x<-1*hard:
                cpu.x -= randint(1, 7)
        except:
            pass
        cpu.x = max(size[0]/2,cpu.x)
        cpu.x = min(size[0],cpu.x)
        for ball in cpuballs:
            pygame.draw.circle(screen, RED, ball, 20)
            ball[1] += 5
            if cpu.collidepoint(ball):
                cpupoints += 1
                if diff < 95:
                    diff += 1
                cpuballs.remove(ball)
            if ball[1]>size[1]:
                cpuballs.remove(ball)
        pygame.draw.rect(screen, GREEN, cpu)
        text(str(cpupoints), size[0] *0.75, 20)
        text(f'{enemy}, use your mouse to get the ball', size[0] *0.75, size[1] * 0.4,10)

        text(str(seconds), size[0] / 2, 20)
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)


async def fish():
    global size, done, name
    balls = [[10, size[1]]]
    cpuballs = [[10+size[0]/2,size[1]]]
    square = pygame.Rect(size[0]/2 - 100, 100, 50, 50)
    cpu = pygame.Rect(size[0] - 100, 100, 50, 50)
    sb = button('||', GREEN, (50, 50), (50, 50))
    started = False
    points = 0
    hard = 10
    cpupoints =0
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
                else:
                    winner = enemy
                print('The winner is ' + winner)
                return winner
                started = True
        distx = mx - square.x
        if randint(0, 50 - diff) == 1:
            balls.append([randint(0, size[0]/2-20), size[1]])
            cpuballs.append([randint(size[0] / 2+20, size[0]), size[1]])
        pygame.draw.line(screen, BLACK, (size[0]/2 - 100, 100), (mx, min(my, 200)))
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
            balls.append([randint(0, size[0] / 2 - 20), size[1]])
            cpuballs.append([randint(size[0]/2+20, size[0]), size[1]])
        try:
            pygame.draw.line(screen, BLACK, (size[0] - 100, 100), (cpuballs[0][0], 200))
        except:
            pass
        for ball in cpuballs:
            pygame.draw.circle(screen, RED, ball, 20)
            ball[1] -= diff / 5 + 1
            if ball[1] <= 200:
                cpuballs.remove(ball)
        if randint(0,10*hard)==7:
            try:
                cpuballs.remove(cpuballs[0])
                cpupoints += 1
            except:
                pass

        pygame.draw.rect(screen, GREEN, square)
        pygame.draw.rect(screen, PURPLE, cpu)
        pygame.draw.line(screen, BLACK, (size[0]/2, 20), (size[0]/2,size[1]))
        text("let's go fishing!", size[0] / 2, size[1] * 0.2, 50)
        text(str(points), size[0]/4, 20)
        text(str(cpupoints), size[0] *0.75, 20)
        text(str(seconds), size[0] / 2, 20)
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)


def loadLevel(level,first = False):
    global behind, tiles, xoffset, yoffset, player
    tiled_map = load_pygame(f'level{lebel}.tmx')
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
    xoffset = 0
    yoffset = 0


async def play():
    global size, done, name, pronouns, player, tiles, map, xoffset, yoffset, behind, key, lebel
    speed = 5
    sb = button('||', GREEN, (50, 50), (50, 50))
    started = False
    portals = [(19, 10)]
    tiles = []
    behind = []
    key = ''
    loadLevel(lebel,True)
    while not started and not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                backup()
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f'({mx // tilesize},{my // tilesize}),')
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
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)


player = Player()
asyncio.run(start())
'''
if randint(0, 2) == 1:
    fish()
else:
    catch()
    '''
asyncio.run(play())
