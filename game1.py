import pygame
import random
import time
import math
import button

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
logo_font = pygame.font.Font('freesansbold.ttf', 30)
spawn = True
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

direction = ''
board_values = [[0 for _ in range(4)] for _ in range(4)]
count = 0
score = 0

file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

bot_btn1 = button.Button('Bot ON', 100, 50, (240, 410), 1, screen, font)
bot_btn2 = button.Button('Bot OFF', 100, 50, (240, 470), 1, screen, font)


start = time.time()
end = 0
seconds = 0


def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


def board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score:  {score}' , True, 'black')
    high_score_text = font.render(f'High score: {high_score}', True, 'black')
    timer = font.render(f'Time: {seconds} seconds', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    screen.blit(timer, (10,490))

    #instructions = font.render('Press R to restart', True, 'black')
    #instructions2 = font.render('Press ESC to return to menu', True, 'black')
    #screen.blit(instructions, (10, 530))
    #screen.blit(instructions2, (10, 570))



def new_board(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True

    return board, full


def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


def take_turn(direction, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direction == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i-shift-1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    if direction == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direction == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direction == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direction  == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


bot = False
player = True
run = True
while run:
        timer.tick(fps)
        screen.fill('gray')
        board()
        draw_pieces(board_values)
        seconds = math.trunc((start - end) * (-1))
        bot_btn1.draw()
        bot_btn2.draw()
        if spawn or count < 2:
            board_values, game_over = new_board(board_values)
            spawn = False
            count += 1

        if direction != '':
            board_values = take_turn(direction, board_values)
            direction = ''
            spawn = True

        if game_over:
            draw_over()
            if high_score > init_high:
                file = open('high_score', 'w')
                file.write(f'{high_score}')
                file.close()
                init_high = high_score

        if bot_btn1.check_click():
            bot = True
            player = False

        if bot_btn2.check_click():
            bot = False
            player = True

        if bot:
            actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            direction = random.choice(actions)

            for action in pygame.event.get():
                if action.type == pygame.KEYUP:
                    if game_over:
                        if action.key == pygame.K_RETURN:
                            board_values = [[0 for _ in range(4)] for _ in range(4)]
                            spawn_new = True
                            init_count = 0
                            score = 0
                            start = time.time()
                            ends = 0
                            direction = ''
                            game_over = False
        end = time.time()
        if player:
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    run = False
                if action.type == pygame.KEYUP:
                    if action.key == pygame.K_UP:
                        direction = 'UP'
                    if action.key == pygame.K_DOWN:
                        direction = 'DOWN'
                    if action.key == pygame.K_LEFT:
                        direction = 'LEFT'
                    if action.key == pygame.K_RIGHT:
                        direction = 'RIGHT'
                    if action.key == pygame.K_r:
                        board_values = [[0 for _ in range(4)] for _ in range(4)]
                        spawn_new = True
                        init_count = 0
                        score = 0
                        start = time.time()
                        end = 0
                        direction = ''
                        game_over = False
                    if game_over:
                        if action.key == pygame.K_RETURN:
                            board_values = [[0 for _ in range(4)] for _ in range(4)]
                            spawn = True
                            init_count = 0
                            score = 0
                            direction = ''
                            game_over = False

            if score > high_score:
                high_score = score
                if high_score > init_high:
                    file = open('high_score', 'w')
                    file.write(f'{high_score}')
                    file.close()
                    init_high = high_score

        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                run = False

        pygame.display.flip()
pygame.quit()