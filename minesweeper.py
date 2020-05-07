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
# Sets the starting number of squares
NSQUARES = 10
# Sets the margin between each cell
MARGIN = 5
MENU_SIZE = 40


# Class that holds the game logic          
class Game:
    
    # Array to store game data
    def __init__(self):
        self.grid = [[self.Cell(x, y) for x in range(NSQUARES)] for y in range(NSQUARES)]
        self.init = False
        self.game_lost = False
        self.game_won = False
        self.num_bombs = 10
        self.squares_x = NSQUARES
        self.squares_y = NSQUARES
        self.resize = False
        self.flag_count = 0

    def draw(self):
        self.check_flag_victory()
        # Set the screen background color
        screen.fill(BLACK)
        # Draw the grid
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                color = WHITE
                if self.grid[row][column].is_visible:
                    if self.grid[row][column].has_bomb:
                        color = RED
                    else:
                        color = GRAY
                elif self.grid[row][column].has_flag:
                    color = BLUE
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN + MENU_SIZE,
                                WIDTH,
                                HEIGHT])
                self.grid[row][column].show_text()
        
    # Adjusts the grid when the screen size has changed
    def adjust_grid(self, sizex, sizey):
        global screen
        self.squares_x = (sizex - MARGIN) // (WIDTH + MARGIN)
        self.squares_y = (sizey - MARGIN - MENU_SIZE) // (HEIGHT + MARGIN)
        if self.squares_x < 8:
            self.squares_x = 8
        if self.squares_y < 8:
            self.squares_y = 8
        if self.num_bombs > (self.squares_x * self.squares_y) // 3:
            self.num_bombs = self.squares_x * self.squares_y // 3
        self.grid = [[self.Cell(x, y) for x in range(self.squares_x)] for y in range(self.squares_y)]
        size = ((self.squares_x*(WIDTH + MARGIN) + MARGIN), (self.squares_y*(HEIGHT + MARGIN) + MARGIN + MENU_SIZE))
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    # Makes all cells visible when user loses
    def game_over(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                if self.grid[row][column].has_bomb:
                    self.grid[row][column].is_visible = True
                self.grid[row][column].has_flag = False

    # Changes the number of bombs placed and caps it
    def change_num_bombs(self, bombs):
        self.num_bombs += bombs
        if self.num_bombs < 1:
            self.num_bombs = 1
        elif self.num_bombs > (self.squares_x * self.squares_y) // 3:
            self.num_bombs = self.squares_x * self.squares_y // 3
        restart_game() 

    # Place BOMBS on random places
    def place_bombs(self, row, column):
        bombplaced = 0
        while bombplaced < self.num_bombs:
            x = randrange(self.squares_y)
            y = randrange(self.squares_x)
            if not self.grid[x][y].has_bomb and not (row == x and column == y):
                self.grid[x][y].has_bomb = True
                bombplaced += 1
        self.count_all_bombs()
        if self.grid[row][column].bomb_count != 0:
            restart_game()
            self.place_bombs(row, column)
        
    # Count all bombs next to a cell (3x3) for the entire grid
    def count_all_bombs(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.grid[row][column].count_bombs(self.squares_y, self.squares_x)
    
    # Restarts the game
    def reset_game(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.init = False
                self.grid[row][column].is_visible = False
                self.grid[row][column].has_bomb = False
                self.grid[row][column].bomb_count = 0
                self.grid[row][column].test = False
                self.grid[row][column].has_flag = False
                self.game_lost = False
                self.game_won = False
                self.flag_count = 0

    def check_flag_victory(self):
        total_flags = 0
        count = 0
        total = self.squares_x * self.squares_y
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                if self.grid[row][column].is_visible:
                    count += 1
                if self.grid[row][column].has_flag:
                    total_flags += 1
        if ((total - count) == self.num_bombs) and not self.game_lost:
            self.game_won = True
            for row in range(self.squares_y):
                for column in range(self.squares_x):
                    if self.grid[row][column].has_bomb:
                        self.grid[row][column].has_flag = True
        self.flag_count = total_flags

    # Handle for grid clicks
    def click_handle(self, row, column, button):
        # Mouse left click action
        if button == 1 and self.game_won:
                restart_game()
        elif button == 1 and not self.grid[row][column].has_flag: 
            if not self.game_lost:
                # Place bombs after first click so you never click a bomb first
                if not self.init:
                    self.place_bombs(row, column)
                    self.init = True
                # Set the click square to visible
                self.grid[row][column].is_visible = True
                self.grid[row][column].has_flag = False
                if self.grid[row][column].has_bomb:
                    self.game_over()
                    self.game_lost = True
                if self.grid[row][column].bomb_count == 0 and not self.grid[row][column].has_bomb:
                    self.grid[row][column].open_neighbours(self.squares_y, self.squares_x)
            else:
                self.game_lost = False
                restart_game()
        
        # Mouse right click action
        elif button == 3 and not self.game_won:
            if not self.grid[row][column].has_flag:
                if self.flag_count < self.num_bombs and not self.grid[row][column].is_visible:
                    self.grid[row][column].has_flag = True
            else:
                self.grid[row][column].has_flag = False


    # Game Sub-Class for each Cell of the grid
    class Cell:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.is_visible = False
            self.has_bomb = False
            self.bomb_count = 0
            self.text = ""
            self.test = False
            self.has_flag = False

        # Handle for the number of bombs text
        def show_text(self):
            if self.is_visible:
                if self.bomb_count == 0:
                    self.text = font.render("", True, BLACK)
                else:
                    self.text = font.render(str(self.bomb_count), True, BLACK)
                screen.blit(self.text, (self.x * (WIDTH + MARGIN) + 12, self.y * (HEIGHT + MARGIN) + 10 + MENU_SIZE))
        
        # Counts how many bombs are next to this cell (3x3)
        def count_bombs(self, squaresx, squaresy):
            if not self.test:
                self.test = True
                if not self.has_bomb:
                    for column in range(self.x - 1 , self.x + 2):
                        for row in range(self.y - 1 , self.y + 2):
                            if row >= 0 and row < squaresx and column >= 0 and column < squaresy:
                                if not (column == self.x and row == self.y):
                                    if game.grid[row][column].has_bomb:
                                        self.bomb_count += 1
        
        # Open all cells next to the clicked cell with zero bombs nearby
        def open_neighbours(self, squaresx, squaresy):
            y = self.x
            x = self.y
            for xoff in range(-1, 2):
                for yoff in range(-1, 2):
                    if ((xoff == 0 or yoff == 0) and xoff != yoff
                        and x+xoff >= 0 and y+yoff >=0 and x+xoff < squaresx and y+yoff < squaresy):
                            game.grid[x + xoff][y + yoff].count_bombs(game.squares_y, game.squares_x)
                            if not game.grid[x + xoff][y + yoff].is_visible and not game.grid[x + xoff][y + yoff].has_bomb:  
                                    game.grid[x + xoff][y + yoff].is_visible = True
                                    game.grid[x + xoff][y + yoff].has_flag = False
                                    if game.grid[x + xoff][y + yoff].bomb_count == 0: 
                                        game.grid[x + xoff][y + yoff].open_neighbours(game.squares_y, game.squares_x)


class Menu():

    def __init__(self):
        self.width = pygame.display.get_surface().get_width() - 2*MARGIN
        self.button1 = self.Button(10, 10, 20, 20, "-", 6, -3)
        self.button2 = self.Button(60, 10, 20, 20, "+", 3, -4)
        self.button3 = self.Button(280, 16, 10, 10, "")
        self.button3.background = BLUE
        self.label1 = self.Label(30, 10)
        self.label2 = self.Label(100, 10)
        self.label3 = self.Label(self.width - 50, 10)

    def click_handle(self, obj):
        if self.button1.click_handle():
            obj.change_num_bombs(-1)
        if self.button2.click_handle():
            obj.change_num_bombs(1)
        
    def draw(self, obj):
        self.width = pygame.display.get_surface().get_width() - 2*MARGIN 
        pygame.draw.rect(screen, GRAY, [MARGIN, 0, self.width, MENU_SIZE])
        self.button1.draw(screen)
        self.button2.draw(screen)
        self.button3.draw(screen)
        self.label1.show(screen, game.num_bombs)
        self.label3.show(screen, game.flag_count)
        if obj.game_lost:
            self.label2.show(screen, "Game Over")
        elif obj.game_won:
            self.label2.show(screen, "You Won!")
    

    class Label:
    
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.text = ""
        
        def show(self, surface, value): 
            text = str(value)
            self.text = font.render(text, True, BLACK)     
            surface.blit(self.text, (self.x, self.y))
    

    class Button:

        def __init__(self, x, y, width, height, text, xoff=0, yoff=0):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.background = WHITE
            self.text = text
            self.x_offset = xoff
            self.y_offset = yoff

        def draw(self, surface):
            pygame.draw.ellipse(surface, self.background, [self.x, self.y, self.width, self.height], 0)
            text = font.render(self.text, True, BLACK)     
            surface.blit(text, (self.x + self.x_offset, self.y + self.y_offset))
        
        def click_handle(self):
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[1] > self.y and pos[0] < (self.x + self.width) and pos[1] < (self.y + self.height):
                return True
            else:
                return False

def restart_game():
    global game
    game = Game()

# Initialize pygame and sets screen size and caption
pygame.init()
size = (NSQUARES*(WIDTH + MARGIN) + MARGIN, (NSQUARES*(HEIGHT + MARGIN) + MARGIN) + MENU_SIZE)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper by Raul Vieira")
# Font to use in the entire game
font = pygame.font.Font('freesansbold.ttf', 24)
# Create instances for Game and Menu
game = Game()
menu = Menu()
clock = pygame.time.Clock()
# Main loop
while True:
    for event in pygame.event.get():
        # Closes the game if user clicked the X
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
        # Mouse clicks event
        elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                position = pygame.mouse.get_pos()
                # Change the screen coordinates to grid coordinates and caps max values
                column = position[0] // (WIDTH + MARGIN)
                row = (position[1] - MENU_SIZE) // (HEIGHT + MARGIN)
                if row >= game.squares_y:
                    row = game.squares_y - 1
                if column >= game.squares_x:
                    column = game.squares_x - 1
                if row >= 0:
                    game.click_handle(row, column, event.button)
                else:
                    menu.click_handle(game)
        # Event for screen resize    
        elif event.type == pygame.VIDEORESIZE:
            if game.resize: 
                game.adjust_grid(event.w, event.h)
                restart_game()
            else:  
                game.resize = True
    game.draw()
    menu.draw(game)
    clock.tick(60)
    # Update the screen
    pygame.display.flip()



