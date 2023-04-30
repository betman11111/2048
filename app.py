import pygame
import button
import time
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 800


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
logo_font = pygame.font.Font('freesansbold.ttf', 30)
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

bot1_btn1 = button.Button('Bot ON', 100, 50, (240, 410), 1, screen, font)
bot1_btn2 = button.Button('Bot OFF', 100, 50, (240, 470), 1, screen, font)

bot2_btn1 = button.Button('Bot ON', 100, 50, (240, 510), 1, screen, font)
bot2_btn2 = button.Button('Bot OFF', 100, 50, (240, 570), 1, screen, font)

bot3_btn1 = button.Button('Bot ON', 100, 50, (240, 610), 1, screen, font)
bot3_btn2 = button.Button('Bot OFF', 100, 50, (240, 670), 1, screen, font)


btn1 = button.Button('4x4 Mode', 250, 70, (275, 150), 1, screen, font)
btn2 = button.Button('5x5 Mode', 250, 70, (275, 250), 1, screen, font)
btn3 = button.Button('6x6 Mode', 250, 70, (275, 350), 1, screen, font)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_over():
    pygame.draw.rect(screen, 'black', [250, 240, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (280, 250))
    screen.blit(game_over_text2, (280, 300))


def board(size, score, seconds, high_score):
    pygame.draw.rect(screen, colors['bg'], [(800-size*100)/2, 0, size*100, size*100], 0, 10)
    score_text = font.render(f'Score:  {score}', True, 'black')
    high_score_text = font.render(f'High score: {high_score}', True, 'black')
    clock = font.render(f'Time: {seconds} seconds', True, 'black')
    screen.blit(score_text, (10, 10 + size*100))
    screen.blit(high_score_text, (10, 50 + size*100))
    screen.blit(clock, (10, 90 + size*100))

    instructions = font.render('Press R to restart', True, 'black')
    instructions2 = font.render('Press ESC to return to menu (make sure Bot is OFF)', True, 'black')
    screen.blit(instructions, (10, 130 + size*100))
    screen.blit(instructions2, (10, 170 + size*100))


def new_board(board, size):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, size-1)
        col = random.randint(0, size-1)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True

    return board, full


def draw_pieces(board, size):
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20 + (800-size*100)/2, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57 + (800-size*100)/2, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20 + (800-size*100)/2, i * 95 + 20, 75, 75], 2, 5)


def take_turn(direction, board, size, score):
    merged = [[False for _ in range(size)] for _ in range(size)]
    if direction == 'UP':
        for i in range(size):
            for j in range(size):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] \
                            and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i-shift-1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    if direction == 'UP':
        for i in range(size):
            for j in range(size):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] \
                            and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direction == 'DOWN':
        for i in range(size-1):
            for j in range(size):
                shift = 0
                for q in range(i + 1):
                    if board[size-1 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[size-2 - i + shift][j] = board[size-2 - i][j]
                    board[size-2 - i][j] = 0
                if size-1 - i + shift <= size-1:
                    if board[size-2 - i + shift][j] == board[size-1 - i + shift][j] \
                            and not merged[size-1 - i + shift][j] and not merged[size-2 - i + shift][j]:
                        board[size-1 - i + shift][j] *= 2
                        score += board[size-1 - i + shift][j]
                        board[size-2 - i + shift][j] = 0
                        merged[size-1 - i + shift][j] = True

    elif direction == 'LEFT':
        for i in range(size):
            for j in range(size):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] \
                        and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direction == 'RIGHT':
        for i in range(size):
            for j in range(size):
                shift = 0
                for q in range(j):
                    if board[i][size-1 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][size-1 - j + shift] = board[i][3 - j]
                    board[i][size-1 - j] = 0
                if size - j + shift <= size-1:
                    if board[i][size - j + shift] == board[i][size-1 - j + shift] and not merged[i][size - j + shift] \
                            and not merged[i][size-1 - j + shift]:
                        board[i][size - j + shift] *= 2
                        score += board[i][size - j + shift]
                        board[i][size-1 - j + shift] = 0
                        merged[i][size - j + shift] = True
    return board, score


# board 1
file1 = open('high_score1', 'r')
init_high1 = int(file1.readline())
file1.close()
high_score1 = init_high1
board_values1 = [[0 for _ in range(4)] for _ in range(4)]
direction1 = ''
count1 = 0
start1 = time.time()
end1 = 0
seconds1 = 0
score1 = 0
spawn1 = True
bot1 = False
player1 = True
game_over1 = False

# board 2
file2 = open('high_score2', 'r')
init_high2 = int(file2.readline())
file2.close()
high_score2 = init_high2
board_values2 = [[0 for _ in range(5)] for _ in range(5)]
direction2 = ''
count2 = 0
start2 = time.time()
end2 = 0
seconds2 = 0
score2 = 0
spawn2 = True
bot2 = False
player2 = True
game_over2 = False

# board 3
file3 = open('high_score3', 'r')
init_high3 = int(file3.readline())
file3.close()
high_score3 = init_high3
board_values3 = [[0 for _ in range(6)] for _ in range(6)]
direction3 = ''
count3 = 0
start3 = time.time()
end3 = 0
seconds3 = 0
score3 = 0
spawn3 = True
bot3 = False
player3 = True
game_over3 = False


run = True
state = 'menu'
while run:
    timer.tick(fps)
    screen.fill('gray')
    if state == 'menu':
        draw_text('2048', logo_font, (255, 100, 100), 360, 70)
        draw_text('Made by Aidyn Fatikh', font, 'black', 10, 700)
        btn1.draw()
        btn2.draw()
        btn3.draw()
    if btn1.check_click():
        state = 'game1'
    if btn2.check_click():
        state = 'game2'
    if btn3.check_click():
        state = 'game3'

    if state == 'game1':
        board(4, score1, seconds1, high_score1)
        draw_pieces(board_values1, 4)
        seconds1 = math.trunc((start1 - end1) * (-1))
        bot1_btn1.draw()
        bot1_btn2.draw()
        if spawn1 or count1 < 2:
            board_values1, game_over1 = new_board(board_values1, 4)
            spawn1 = False
            count1 += 1

        if direction1 != '':
            board_values1, score1 = take_turn(direction1, board_values1, 4, score1)
            direction1 = ''
            spawn1 = True

        if game_over1:
            draw_over()
            if high_score1 > init_high1:
                file1 = open('high_score1', 'w')
                file1.write(f'{high_score1}')
                file1.close()
                init_high1 = high_score1

        if bot1_btn1.check_click():
            bot1 = True
            player1 = False

        if bot1_btn2.check_click():
            bot1 = False
            player1 = True

        if bot1:
            actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            direction1 = random.choice(actions)

            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if game_over1:
                        if action.key == pygame.K_RETURN:
                            board_values1 = [[0 for _ in range(4)] for _ in range(4)]
                            spawn_new1 = True
                            init_count1 = 0
                            score1 = 0
                            start1 = time.time()
                            ends1 = 0
                            direction1 = ''
                            game_over1 = False
            if score1 > high_score1:
                high_score1 = score1
                if high_score1 > init_high1:
                    file1 = open('high_score1', 'w')
                    file1.write(f'{high_score1}')
                    file1.close()
                    init_high1 = high_score1
        end1 = time.time()
        if player1:
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if action.key == pygame.K_UP:
                        direction1 = 'UP'
                    if action.key == pygame.K_DOWN:
                        direction1 = 'DOWN'
                    if action.key == pygame.K_LEFT:
                        direction1 = 'LEFT'
                    if action.key == pygame.K_RIGHT:
                        direction1 = 'RIGHT'
                    if action.key == pygame.K_r:
                        board_values1 = [[0 for _ in range(4)] for _ in range(4)]
                        spawn1 = True
                        init_count1 = 0
                        score1 = 0
                        start1 = time.time()
                        end1 = 0
                        direction1 = ''
                        game_over1 = False
                    if action.key == pygame.K_ESCAPE:
                        state = 'menu'

                    if game_over1:
                        if action.key == pygame.K_RETURN:
                            board_values1 = [[0 for _ in range(4)] for _ in range(4)]
                            spawn1 = True
                            start1 = time.time()
                            end1 = 0
                            init_count1 = 0
                            score1 = 0
                            direction1 = ''
                            game_over1 = False

            if score1 > high_score1:
                high_score1 = score1
                if high_score1 > init_high1:
                    file1 = open('high_score1', 'w')
                    file1.write(f'{high_score1}')
                    file1.close()
                    init_high1 = high_score1
    if state == 'game2':
        board(5, score2, seconds2, high_score2)
        draw_pieces(board_values2, 5)
        seconds2 = math.trunc((start2 - end2) * (-1))
        bot2_btn1.draw()
        bot2_btn2.draw()
        if spawn2 or count2 < 2:
            board_values2, game_over2 = new_board(board_values2, 5)
            spawn2 = False
            count2 += 1

        if direction2 != '':
            board_values2, score2 = take_turn(direction2, board_values2, 5, score2)
            direction2 = ''
            spawn2 = True

        if game_over2:
            draw_over()
            if high_score2 > init_high2:
                file2 = open('high_score2', 'w')
                file2.write(f'{high_score2}')
                file2.close()
                init_high2 = high_score2

        if bot2_btn1.check_click():
            bot2 = True
            player2 = False

        if bot2_btn2.check_click():
            bot2 = False
            player2 = True

        if bot2:
            actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            direction2 = random.choice(actions)

            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if game_over2:
                        if action.key == pygame.K_RETURN:
                            board_values2 = [[0 for _ in range(5)] for _ in range(5)]
                            spawn_new2 = True
                            init_count2 = 0
                            score2 = 0
                            start2 = time.time()
                            ends2 = 0
                            direction2 = ''
                            game_over2 = False

            if score2 > high_score2:
                high_score2 = score2
                if high_score2 > init_high2:
                    file2 = open('high_score2', 'w')
                    file2.write(f'{high_score2}')
                    file2.close()
                    init_high2 = high_score2
        end2 = time.time()
        if player2:
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if action.key == pygame.K_UP:
                        direction2 = 'UP'
                    if action.key == pygame.K_DOWN:
                        direction2 = 'DOWN'
                    if action.key == pygame.K_LEFT:
                        direction2 = 'LEFT'
                    if action.key == pygame.K_RIGHT:
                        direction2 = 'RIGHT'
                    if action.key == pygame.K_r:
                        board_values2 = [[0 for _ in range(5)] for _ in range(5)]
                        spawn2 = True
                        init_count2 = 0
                        score2 = 0
                        start2 = time.time()
                        end2 = 0
                        direction2 = ''
                        game_over2 = False
                    if action.key == pygame.K_ESCAPE:
                        state = 'menu'

                    if game_over2:
                        if action.key == pygame.K_RETURN:
                            board_values2 = [[0 for _ in range(5)] for _ in range(5)]
                            spawn2 = True
                            seconds2 = 0
                            start2 = time.time()
                            ends2 = 0
                            init_count2 = 0
                            score2 = 0
                            direction2 = ''
                            game_over2 = False

            if score2 > high_score2:
                high_score2 = score2
                if high_score2 > init_high2:
                    file2 = open('high_score2', 'w')
                    file2.write(f'{high_score2}')
                    file2.close()
                    init_high2 = high_score2
    if state == 'game3':
        board(6, score3, seconds3, high_score3)
        draw_pieces(board_values3, 6)
        seconds3 = math.trunc((start3 - end3) * (-1))
        bot3_btn1.draw()
        bot3_btn2.draw()
        if spawn3 or count3 < 2:
            board_values3, game_over3 = new_board(board_values3, 6)
            spawn3 = False
            count3 += 1

        if direction3 != '':
            board_values3, score3 = take_turn(direction3, board_values3, 6, score3)
            direction3 = ''
            spawn3 = True

        if game_over3:
            draw_over()
            if high_score3 > init_high3:
                file3 = open('high_score3', 'w')
                file3.write(f'{high_score3}')
                file3.close()
                init_high3 = high_score3

        if bot3_btn1.check_click():
            bot3 = True
            player3 = False

        if bot3_btn2.check_click():
            bot3 = False
            player3 = True

        if bot3:
            actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            direction3 = random.choice(actions)

            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if game_over3:
                        if action.key == pygame.K_RETURN:
                            board_values3 = [[0 for _ in range(6)] for _ in range(6)]
                            spawn_new3 = True
                            init_count3 = 0
                            score3 = 0
                            start3 = time.time()
                            ends3 = 0
                            direction3 = ''
                            game_over3 = False

            if score3 > high_score3:
                high_score3 = score3
                if high_score3 > init_high3:
                    file3 = open('high_score3', 'w')
                    file3.write(f'{high_score3}')
                    file3.close()
                    init_high3 = high_score3
        end3 = time.time()
        if player3:
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if action.key == pygame.K_UP:
                        direction3 = 'UP'
                    if action.key == pygame.K_DOWN:
                        direction3 = 'DOWN'
                    if action.key == pygame.K_LEFT:
                        direction3 = 'LEFT'
                    if action.key == pygame.K_RIGHT:
                        direction3 = 'RIGHT'
                    if action.key == pygame.K_r:
                        board_values3 = [[0 for _ in range(6)] for _ in range(6)]
                        spawn3 = True
                        init_count3 = 0
                        score3 = 0
                        start3 = time.time()
                        end3 = 0
                        direction3 = ''
                        game_over3 = False
                    if action.key == pygame.K_ESCAPE:
                        state = 'menu'

                    if game_over3:
                        if action.key == pygame.K_RETURN:
                            board_values3 = [[0 for _ in range(6)] for _ in range(6)]
                            seconds3 = 0
                            spawn3 = True
                            init_count3 = 0
                            start3 = time.time()
                            end3 = 0
                            score3 = 0
                            direction3 = ''
                            game_over3 = False

            if score3 > high_score3:
                high_score3 = score3
                if high_score3 > init_high3:
                    file3 = open('high_score3', 'w')
                    file3.write(f'{high_score3}')
                    file3.close()
                    init_high3 = high_score3

    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
