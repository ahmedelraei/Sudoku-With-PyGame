import pygame
import sys
import time
from threading import Thread

pygame.font.init()

# Colors
GREEN = (0,100,0)


class Board:
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

    def __init__(self, screen):
        self.rows = 9
        self.cols = 9
        self.screen = screen
        self.cells = [[Cell(self.grid[i][j], i, j) for j in range(9)] for i in range(9)]
        self.selected = None
        self.model = None
        self.update_model()
    
    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    def gameover(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True

    
    def draw(self):
        pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(15, 15, 720, 720), 10)

        i = 1
        while (i * 80) < 720:
            line_width = 5 if i % 3 > 0 else 10
            pygame.draw.line(self.screen, pygame.Color('white'), pygame.Vector2((i * 80 + 15), 15), pygame.Vector2((i * 80 + 15), 735), line_width)
            pygame.draw.line(self.screen, pygame.Color('white'), pygame.Vector2(15, (i * 80 + 15)), pygame.Vector2(735, (i * 80 + 15)), line_width)
            i += 1

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.screen)
    

    def sketch(self, val):
        row, col = self.selected
        self.cells[row][col].temp_value = val
    

    def select(self, row, col):
        # Clears selection
        try:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.cells[i][j].selected = False

            self.cells[row][col].selected = True
            self.selected = (row, col)
        except IndexError:
            pass
    
    
    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].temp_value = 0


    def insert(self, val):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].value = val
            self.update_model()

            if self.validate(val, (row,col)) and self.solve():
                return True
            else:
                self.cells[row][col].value = 0
                self.cells[row][col].temp_value = 0
                self.update_model()
                return False

    
    def validate(self, num, pos):
        # Check row
        for y in range(len(self.model[0])):
            if self.model[pos[0]][y] == num and pos[1] != y:
                return False

        # Check column
        for x in range(len(self.model)):
            if self.model[x][pos[1]] == num and pos[0] != x:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for x in range(box_y*3, box_y*3 + 3):
            for y in range(box_x*3, box_x*3 + 3):
                if self.model[x][y] == num and (x,y) != pos:
                    return False
        
        return True


    def locate_empty(self, board):
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == 0:
                    return (x, y)
        
        return None


    def solve(self):
        find = self.locate_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.validate(i, (row,col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0
        
        return False
    
    def solve_visualization(self):
        find = self.locate_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.validate(i, (row,col)):
                self.model[row][col] = i
                self.cells[row][col].value = i
                t = Thread(target=self.cells[row][col].visualize(self.screen, True))
                t.daemon = True
                t.start()
                #self.cells[row][col].visualize(self.screen, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(50)
                if self.solve_visualization():
                    return True

                self.model[row][col] = 0
                self.cells[row][col].value = 0
                self.update_model()
                self.cells[row][col].visualize(self.screen, False)
                pygame.display.update()
                pygame.time.delay(50)
        
        return False

class Cell:
    def __init__(self, value, row, col):
        self.temp_value = 0
        self.value = value
        self.row = row
        self.col = col
        self.selected = False

    
    def draw(self, screen):
        offset = 35
        font = pygame.font.SysFont(None, 80)
        if self.temp_value != 0 and self.value == 0:
            num_text = font.render(str(self.temp_value), True, pygame.Color('white'))
            screen.blit(num_text, pygame.Vector2((self.row * 80) + offset + 4, (self.col * 80) + offset - 2))

        elif self.value != 0:
            num_text = font.render(str(self.value), True, pygame.Color('white'))
            screen.blit(num_text, pygame.Vector2((self.row * 80) + offset + 4, (self.col * 80) + offset - 2))
        
        if self.selected:
            pygame.draw.rect(screen, pygame.Color('yellow'), pygame.Rect(15 + self.row * 80, 15 + self.col * 80, 80, 80), 10)
    

    def visualize(self, screen, bool):
        fnt = pygame.font.SysFont(None, 80)
        offset = 35

        gap = 720 / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(screen, GREEN, (x + 15, y + 15, gap, gap), 0)
        
        text = fnt.render(str(self.value), 1, (255, 255, 255))
        screen.blit(text, pygame.Vector2((self.row * gap) + offset + 4, (self.col * gap) + offset - 2))
        if bool:
            pygame.draw.rect(screen, (0, 255, 0), (x + 15, y + 15, gap, gap), 3)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x + 15, y + 15, gap, gap), 3)



def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    timer = f'{str(minute)}:{str(sec)}'
    return timer

def redraw_window(screen, board, time, strikes):
    screen.fill(GREEN)
    fnt = pygame.font.SysFont(None, 80)
    
    # Draw time
    text = fnt.render("Time: " + format_time(time), True, pygame.Color('white'))
    screen.blit(text, pygame.Vector2(470,770))

    # Draw Strikes
    text = fnt.render("X " * strikes, True, (255, 0, 0))
    screen.blit(text, pygame.Vector2(35,770))

    # Draw grid and board
    board.draw()

def main():
    SCREEN_SIZE = 750, 850
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Sudoku')
    board = Board(screen)
    key = ''
    start = time.time()
    strikes = 0

    while 1:
        timer = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_row = event.pos[0] // 80
                clicked_col = event.pos[1] // 80

                board.select(clicked_row, clicked_col)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cells[i][j].temp_value != 0:
                        if board.insert(board.cells[i][j].temp_value):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.gameover():
                            print("Game over")

                if board.selected and key != None:
                    board.sketch(key)
                
                if event.key == pygame.K_SPACE:
                    board.solve_visualization()

        t = Thread(target=redraw_window(screen, board, timer, strikes))
        t.daemon = True
        t.start()
        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()