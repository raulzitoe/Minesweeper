import pygame
import sys
from random import random, randrange

pygame.init()

# Colors used
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)

# Sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# Sets the number of squares
NSQUARES = 10

# Number of Bombs
BOMBS = 10

# Sets the margin between each cell
MARGIN = 5

size = (NSQUARES*(WIDTH + MARGIN) + MARGIN, (NSQUARES*(HEIGHT + MARGIN) + MARGIN))
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

# Set title of screen
pygame.display.set_caption("Minesweeper By Raul")

font = pygame.font.Font('freesansbold.ttf', 24) 

class Cell:
    visible = False
    color = RED
    bomb = False
    bomb_count = 0
    text = ""
    xtext = 0
    ytext = 0
    test = False

    def __init__(self, x, y):
        self.xtext = x
        self.ytext = y

    def show_text(self):
        if self.visible == True:
            if self.bomb_count == 0:
                 self.text = font.render("", True, BLACK)
            else:
                 self.text = font.render(str(self.bomb_count), True, BLACK)
           
            screen.blit(self.text, (self.xtext * (WIDTH + MARGIN) + 12, self.ytext * (HEIGHT + MARGIN) + 10))
    
    def count_bombs(self):
        if self.test == False:
            self.test = True
            if not self.bomb == True:
                for column in range(self.xtext - 1 , self.xtext + 2):
                    for row in range(self.ytext - 1 , self.ytext + 2):
                        if row >= 0 and row < NSQUARES and column >= 0 and column < NSQUARES:
                            if not (column == self.xtext and row == self.ytext):
                                if game.grid[row][column].bomb == True:
                                    self.bomb_count += 1
    
    def open_neighbours(self):
        y = self.xtext
        x = self.ytext
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                if ((xoff == 0 or yoff == 0) and xoff != yoff
                    and x+xoff >= 0 and y+yoff >=0 and x+xoff < NSQUARES and y+yoff < NSQUARES):
                        game.grid[x + xoff][y + yoff].count_bombs()
                        
                        if (game.grid[x + xoff][y + yoff].visible == False 
                            and game.grid[x + xoff][y + yoff].bomb == False):
                                
                                game.grid[x + xoff][y + yoff].visible = True
                                
                                if game.grid[x + xoff][y + yoff].bomb_count == 0: 
                                    game.grid[x + xoff][y + yoff].open_neighbours()
            
class Game:
    init = False
    # Array to store game data
    def __init__(self):
        self.grid = [[Cell(x, y) for x in range(NSQUARES)] for y in range(NSQUARES)]
        
    # Makes all cells visible when user loses
    def game_over(self):
        for row in range(NSQUARES):
            for column in range(NSQUARES):
                self.grid[row][column].visible = True

    # Place BOMBS on random places
    def place_bombs(self, row, column):
        bombplaced = 0
        while bombplaced < BOMBS:
            x = randrange(NSQUARES)
            y = randrange(NSQUARES)
            if not self.grid[x][y].bomb and not (row == x and column == y):
                self.grid[x][y].bomb = True
                bombplaced += 1

    def count_all_bombs(self):
        for row in range(NSQUARES):
            for column in range(NSQUARES):
                self.grid[row][column].count_bombs()

game = Game()


done = False
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            if row >= NSQUARES:
                row = NSQUARES - 1
            if column >= NSQUARES:
                column = NSQUARES - 1
            # Place bombs after first click so you never click a bomb first
            if game.init == False:
                game.init = True
                game.place_bombs(row, column)
                game.count_all_bombs()
            # Set that location to one
            game.grid[row][column].visible = True
            if game.grid[row][column].bomb == True:
                game.game_over()
            if game.grid[row][column].bomb_count == 0 and game.grid[row][column].bomb == False:
                game.grid[row][column].open_neighbours()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)
            screen.fill(WHITE)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(NSQUARES):
        for column in range(NSQUARES):
            color = WHITE
            if game.grid[row][column].visible == True:
                if game.grid[row][column].bomb == True:
                    color = RED
                else:
                    color = GRAY
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            game.grid[row][column].show_text()

    clock.tick(60)
    # Update the screen
    pygame.display.flip()

pygame.quit()



