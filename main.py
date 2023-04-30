import pygame
import button
import time
import random
import math

pygame.init()

WIDTH = 400
HEIGHT = 400


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
logo_font = pygame.font.Font('freesansbold.ttf', 30)
run = True
menu = True


btn1 = button.Button('4x4 Mode', 200, 50, (105, 120), 1, screen, font)
btn2 = button.Button('5x5 Mode', 200, 50, (105, 190), 1, screen, font)
btn3 = button.Button('6x6 Mode', 200, 50, (105, 260), 1, screen, font)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


run = True
state = 'menu'
while run:
    timer.tick(fps)
    screen.fill('gray')
    if state == 'menu':
        draw_text('2048', logo_font, (255, 100, 100), 160, 70)
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
        from game1 import board
        board()
    if state == 'game2':
        from game2 import board
        board()
    if state == 'game3':
        from game3 import board
        board()

    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
