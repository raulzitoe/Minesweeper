import pygame
import sys
from random import randrange

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

# Sets the margin between each cell
MARGIN = 5

# Initialize pygame and sets screen size and caption
pygame.init()
size = (NSQUARES*(WIDTH + MARGIN) + MARGIN, (NSQUARES*(HEIGHT + MARGIN) + MARGIN))
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper By Raul")
font = pygame.font.Font('freesansbold.ttf', 24) 

# Class for each Cell of the game
class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False
        self.bomb = False
        self.bomb_count = 0
        self.text = ""
        self.test = False

    # Handle the number of bombs text
    def show_text(self):
        if self.visible == True:
            if self.bomb_count == 0:
                 self.text = font.render("", True, BLACK)
            else:
                 self.text = font.render(str(self.bomb_count), True, BLACK)
           
            screen.blit(self.text, (self.x * (WIDTH + MARGIN) + 12, self.y * (HEIGHT + MARGIN) + 10))
    
    # Counts how many bombs are next to this cell (3x3)
    def count_bombs(self, squaresx, squaresy):
        if self.test == False:
            self.test = True
            if not self.bomb == True:
                for column in range(self.x - 1 , self.x + 2):
                    for row in range(self.y - 1 , self.y + 2):
                        if row >= 0 and row < squaresx and column >= 0 and column < squaresy:
                            if not (column == self.x and row == self.y):
                                if game.grid[row][column].bomb == True:
                                    self.bomb_count += 1
    
    def open_neighbours(self, squaresx, squaresy):
        y = self.x
        x = self.y
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                if ((xoff == 0 or yoff == 0) and xoff != yoff
                    and x+xoff >= 0 and y+yoff >=0 and x+xoff < squaresx and y+yoff < squaresy):
                        game.grid[x + xoff][y + yoff].count_bombs(game.squares_y, game.squares_x)
                        
                        if (game.grid[x + xoff][y + yoff].visible == False 
                            and game.grid[x + xoff][y + yoff].bomb == False):
                                
                                game.grid[x + xoff][y + yoff].visible = True
                                
                                if game.grid[x + xoff][y + yoff].bomb_count == 0: 
                                    game.grid[x + xoff][y + yoff].open_neighbours(game.squares_y, game.squares_x)

# Class that holds the game logic          
class Game:
    
    # Array to store game data
    def __init__(self):
        self.grid = [[Cell(x, y) for x in range(NSQUARES)] for y in range(NSQUARES)]
        self.init = False
        self.game_lost = False
        self.num_bombs = 10
        self.squares_x = NSQUARES
        self.squares_y = NSQUARES
        self.resize = False

    def adjust_grid(self, sizex, sizey):
        print("ADJUST GRID CALLED")
        self.squares_x = (sizex - MARGIN) // (WIDTH + MARGIN)
        self.squares_y = (sizey - MARGIN) // (HEIGHT + MARGIN)
        print(str(self.squares_x) + " - " + str(self.squares_y))
        self.grid = [[Cell(x, y) for x in range(self.squares_x)] for y in range(self.squares_y)]

    # Makes all cells visible when user loses
    def game_over(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.grid[row][column].visible = True

    # Place BOMBS on random places
    def place_bombs(self, row, column):
        bombplaced = 0
        while bombplaced < self.num_bombs:
            x = randrange(self.squares_y)
            y = randrange(self.squares_x)
            if not self.grid[x][y].bomb and not (row == x and column == y):
                self.grid[x][y].bomb = True
                bombplaced += 1
        self.count_all_bombs()
        if self.grid[row][column].bomb_count != 0:
            self.reset_game()
            self.place_bombs(row, column)
        
    # Count all bombs next to a cell (3x3) for the entire grid
    def count_all_bombs(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.grid[row][column].count_bombs(self.squares_y, self.squares_x)
    
    def reset_game(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.init = False
                self.grid[row][column].visible = False
                self.grid[row][column].bomb = False
                self.grid[row][column].bomb_count = 0
                self.grid[row][column].test = False

    def click_handle(self, row, column):
        if self.game_lost == False:

            # Place bombs after first click so you never click a bomb first
            if self.init == False:
                self.place_bombs(row, column)
                self.init = True

            # Set the click square to visible
            self.grid[row][column].visible = True
            if self.grid[row][column].bomb == True:
                self.game_over()
                self.game_lost = True
            if self.grid[row][column].bomb_count == 0 and self.grid[row][column].bomb == False:
                self.grid[row][column].open_neighbours(self.squares_y, self.squares_x)
        else:
            self.game_lost = False
            self.reset_game()


game = Game()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                position = pygame.mouse.get_pos()
        
                # Change the screen coordinates to grid coordinates
                column = position[0] // (WIDTH + MARGIN)
                row = position[1] // (HEIGHT + MARGIN)
                print("Row: " + str(row) + " - Column: " + str(column))
                if row >= game.squares_y:
                    row = game.squares_y
                if column >= game.squares_x:
                    column = game.squares_x
                game.click_handle(row, column)
            
        elif event.type == pygame.VIDEORESIZE:
            if game.resize == True:
                screen = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)
                screen.fill(WHITE)
                game.adjust_grid(event.w, event.h)
                game.reset_game()
            else:  
                game.resize = True

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(game.squares_y):
        for column in range(game.squares_x):
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



