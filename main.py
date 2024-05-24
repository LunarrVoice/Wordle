import word_lists
import random
import pygame
import pygame.freetype

pygame.init()

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

# colors
WHITE = (248, 248, 248)
BLACK = (0, 0, 0)
BACKGROUND = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GREY = (58, 58, 60)
LIGHTGREY = (129, 131, 132)

solution = random.choice(word_lists.SOLUTION_LIST).upper()

board = []
typed = []

class Square:
    def __init__(self, name, x, y, value="empty"):
        self.name = name
        self.x = (50 * x) + (30 * x) + 125
        self.y = (50 * y) + (30 * y) - 50
        self.value = value
        
    def draw_square(self):
        if self.value == "empty":
            pygame.draw.rect(SCREEN, LIGHTGREY, (self.x - 1, self.y - 1, 72, 72))
            pygame.draw.rect(SCREEN, BACKGROUND, (self.x, self.y, 70, 70))
        elif self.value == "green":
            pygame.draw.rect(SCREEN, GREEN, (self.x, self.y, 70, 70))
        elif self.value == "yellow":
            pygame.draw.rect(SCREEN, YELLOW, (self.x, self.y, 70, 70))
        elif self.value == "grey":
            pygame.draw.rect(SCREEN, GREY, (self.x, self.y, 70, 70))
        
    def draw_text(self, text):
        draw_text(SCREEN, text, WHITE, self.x + 35, self.y + 35, 44)
        
     
def init_board(letters, guesses):
    global board, typed
    
    board = [[None for x in range(letters)] for x in range(guesses)]
    
    for letter in range(letters):
        for guess in range(guesses):
            object_name = f"square{letter + 1}{guess + 1}"
            board[guess][letter] = Square(object_name, letter + 1, guess + 1)
    
               
def update_board():
    for x, row in enumerate(board):
        for y, obj in enumerate(row):
            obj.draw_square()
            obj.draw_text(typed[x][y])
               
                    
def draw_rounded_rect(surface, color, rect, radius):
    x, y, w, h = rect
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))           


def draw_text(surface, text, color, x, y, font_size):
    font = pygame.freetype.SysFont("clear sans", font_size)
    text_surface, _ = font.render(text, color)
    
    #anchor to center
    text_width, text_height = text_surface.get_size()
    x -= text_width / 2
    y -= text_height / 2
    
    surface.blit(text_surface, (x, y))


def check(guess_input, guess_number):
    letters = ["", "", "", "", ""]
    
    for x in range(5):
        if solution[x] == guess_input[x]:
            for y, row in enumerate(board):
                for z, obj in enumerate(row):
                    if y == guess_number:
                        if z == x:
                            obj.value = "green"
                            letters[x] = "green"
                    
    for x in range(5):
        for y in range(5):
            if solution[y] == guess_input[x]:
                if letters[x] == "":
                    for y, row in enumerate(board):
                        for z, obj in enumerate(row):
                            if y == guess_number:
                                if z == x:
                                    obj.value = "yellow"
                                    letters[x] = "yellow"
                    break
                elif letters[x] == "green":
                    break
    
    for x in range(5):
        if letters[x] == "":
            for y, row in enumerate(board):
                for z, obj in enumerate(row):
                    if y == guess_number:
                        if z == x:
                            obj.value = "grey"

    if letters == ["green", "green", "green", "green", "green"]:
        return "win"
    
    return letters


def main():
    global board, typed
    
    typed = [[None for x in range(5)] for x in range(6)]
    guess_number = 0
    init_board(5, 6)
    
    while True:
        SCREEN.fill(BACKGROUND)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    found = False
                    atrow = ""
                    atcol = ""
                    for x, row in enumerate(typed):
                        for y, element in enumerate(row):
                            if element is None:
                                atrow = x
                                atcol = y
                                found = True
                                break
                        if found:
                            break
                    if atcol != 0:
                        typed[atrow][atcol - 1] = None
                    elif atrow != 0:
                        if atrow > guess_number:
                            typed[atrow - 1][4] = None
                
                elif event.key == pygame.K_RETURN:
                    valid = True
                    guess_input = ""
                    for element in typed[guess_number]:
                        if element is None:
                            valid = False
                            break
                        else:
                            guess_input += element
                    if valid:
                        with open("words.txt", "r") as file:
                            for line in file:
                                if guess_input in line.upper():
                                    check(guess_input, guess_number)
                                    guess_number += 1
      
                else:
                    if event.unicode.isalpha():
                        found = False
                        for x, row in enumerate(typed):
                            for y, element in enumerate(row):
                                if element is None:
                                    if x == guess_number:
                                        typed[x][y] = event.unicode.capitalize()
                                    found = True
                                    break
                            if found:
                                break
        
        update_board()
        
        pygame.display.flip()


main()

    


