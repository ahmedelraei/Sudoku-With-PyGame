import pygame
import sys

from pygame.display import flip

pygame.init()

SCREEN_SIZE = 750, 750
screen = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.SysFont(None, 80)
# Colors
GREEN = (0,100,0)


grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

def draw_bg():
    screen.fill(GREEN)
    pygame.draw.rect(screen, pygame.Color('white'), pygame.Rect(15, 15, 720, 720), 10)

    i = 1
    while (i * 80) < 720:
        line_width = 5 if i % 3 > 0 else 10
        pygame.draw.line(screen, pygame.Color('white'), pygame.Vector2((i * 80 + 15), 15), pygame.Vector2((i * 80 + 15), 735), line_width)
        pygame.draw.line(screen, pygame.Color('white'), pygame.Vector2(15, (i * 80 + 15)), pygame.Vector2(735, (i * 80 + 15)), line_width)
        i += 1

        
    board()

def board():
    offset = 35
    for i in range(9):
        for j in range(9):
            num_text = font.render(str(grid[i][j]), True, pygame.Color('white'))
            screen.blit(num_text, pygame.Vector2((j * 80) + offset + 4, (i * 80) + offset - 2))

def select_cube(x, y):
    draw_bg()
    pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(15 + x * 80, 15 + y * 80, 80, 80), 10)

def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_row = event.pos[0] // 80
            clicked_col = event.pos[1] // 80

            select_cube(clicked_row, clicked_col)

        pygame.display.update()



draw_bg()
while 1:
    game_loop()