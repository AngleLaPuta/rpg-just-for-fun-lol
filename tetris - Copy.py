import math
import asyncio

import pygame
from copy import deepcopy
from random import choice, randrange, randint
async def main():
    global screen
    W, H = 8, 13
    TILE = 32
    GAME_RES = W * TILE, H * TILE
    RES = 700, 500
    FPS = 60
    height = 3

    pygame.init()
    screen = pygame.display.set_mode(RES)
    game_sc = pygame.Surface(GAME_RES)
    ai_sc = pygame.Surface(GAME_RES)
    clock = pygame.time.Clock()

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]

    aifigures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    aifigure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    aifield = [[0 for i in range(W)] for j in range(H)]

    anim_count, anim_speed, anim_limit = 0, 30, 2000
    aianim_count, aianim_speed, aianim_limit = 0, 30, 2000
    rot = False

    get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    aifigure, ainext_figure = deepcopy(choice(aifigures)), deepcopy(choice(aifigures))
    color, next_color = get_color(), get_color()
    aicolor, ainext_color = get_color(), get_color()
    ax = 0
    score, lines = 0, 0
    aiscore,ailines=0,0
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
        screen.fill((0, 0, 0))
        dx, rotate = 0, False
        dy = 1
        screen.blit(game_sc, (20, 20))
        screen.blit(ai_sc, (RES[0]/2+20, 20))
        # delay for full lines
        #for i in range(lines):
            #pygame.time.wait(200)
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
                    anim_limit=100
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
        anim_count += anim_speed*5
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
            for ax in [-1,1,0]:
                for rot in [True,False]:
                    for ay in [-1,-2,-3]:
                        for i in range(4):
                            aifigure[i].y =he[i]
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
                                maxcount = max(maxcount, (count** row)- height**height)
                                line -= 1
                            else:
                                aianim_speed += 3
                                lines += 1
                        for y in range(H):
                            for x in range(W):
                                if aifield[y][x] !=0:
                                    height = min(height, y)
                        height = H-height
                        # COMPUTE ATTEMPT SCORE
                        empty_space_penalty = 0
                        for i in range(4):
                            if aifield[aifigure[i].y][aifigure[i].x]==0:
                                empty_space_penalty += 1
                        attempt_score = scores[lines]-height+maxcount-len(holes) - empty_space_penalty

                        # call minimax function to compute the score for the move
                        attempt_score = minimax(aifigure, 4, -math.inf, math.inf, False)

                        # IF BEST SCORE, STORE BEST MOVE
                        if attempt_score > best_score:
                            #if height != H:
                            print(attempt_score)
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
                    score+=aiscore//2
                    aiscore -= aiscore//2
                    for i_rect in grid:
                        pygame.draw.rect(ai_sc, get_color(), i_rect)
                        screen.blit(ai_sc, (RES[0] / 2 + 20, 20))
                        pygame.display.flip()
                        clock.tick(200)
            # AI NOW USES BEST MOVE, RATHER THAN RANDOM MOVE
            # ADDED DEEP COPY TO STORE BEST MOVE


        # draw next figure
        #for i in range(4):
        #    figure_rect.x = next_figure[i].x * TILE + 380
        #    figure_rect.y = next_figure[i].y * TILE + 185
        #    pygame.draw.rect(screen, next_color, figure_rect)

        # game over
        for i in range(W):
            if field[0][i]:
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                aiscore+=score//2
                score -= score//2
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    screen.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
        text(str(score), RES[0] / 4, 20)
        text(str(aiscore), RES[0] * 0.75, 20)
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)
asyncio.run(main())