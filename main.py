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
keyboard = []

KEYS = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', None],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', None, None, None]
]


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
        
     
class Keyboard:
    def __init__(self, name, key, x, y, key_width, key_height, value="empty"):
        self.name = name
        self.key = key
        self.x = x 
        self.y = y
        self.key_width = key_width
        self.key_height = key_height
        self.value = value
        
    def draw_keyboard(self):
        if self.value == "empty":
            draw_rounded_rect(SCREEN, LIGHTGREY, (self.x, self.y, self.key_width, self.key_height), 6)
        elif self.value == "green":
            draw_rounded_rect(SCREEN, GREEN, (self.x, self.y, self.key_width, self.key_height), 6)
        elif self.value == "yellow":
            draw_rounded_rect(SCREEN, YELLOW, (self.x, self.y, self.key_width, self.key_height), 6)
        elif self.value == "grey":
            draw_rounded_rect(SCREEN, GREY, (self.x, self.y, self.key_width, self.key_height), 6)
        draw_text(SCREEN, self.key, WHITE, self.x + 25, self.y + 27, 24)
                
    def get_key_at_pos(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.key_width and self.y <= y <= self.y + self.key_height:
            return self.key
             
        
def init_board(letters, guesses):
    global board
    
    board = [[None for x in range(letters)] for x in range(guesses)]
    
    for letter in range(letters):
        for guess in range(guesses):
            object_name = f"square{letter + 1}{guess + 1}"
            board[guess][letter] = Square(object_name, letter + 1, guess + 1)
    
    
def init_keyboard():
    global keyboard
    
    keyboard = [[None for x in range(10)] for x in range(3)]
    
    start_x = 120
    start_y = 520 
    key_width = 50 
    key_height = 57
    margin = 7
    stagger_offset=30
    
    for row in range(3):
        row_start_x = start_x + row * stagger_offset
        for col in range(10):
            x = row_start_x + (key_width + margin) * col
            y = start_y + (key_height + margin) * row
            key = KEYS[row][col]
            object_name = f"key{col}{row}"
            keyboard[row][col] = Keyboard(object_name, key, x, y, key_width, key_height)
    
               
def update_board():
    for x, row in enumerate(board):
        for y, obj in enumerate(row):
            obj.draw_square()
            obj.draw_text(typed[x][y])
               

def update_keyboard():
    for x, row in enumerate(keyboard):
        for y, obj in enumerate(row):
            if KEYS[x][y] == None:
                pass
            else:
                obj.draw_keyboard()

                    
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
                            letters[x] = "grey"

    for x in range(5):
        for y, row in enumerate(keyboard):
            for z, obj in enumerate(row):
                if guess_input[x] == KEYS[y][z]:
                    obj.value = letters[x]

    if letters == ["green", "green", "green", "green", "green"]:
        return "win"
    
    return letters


def main():
    global board, typed

    typed = [[None for x in range(5)] for x in range(6)]
    guess_number = 0
    init_board(5, 6)
    init_keyboard()
    
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
                            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    pos = pygame.mouse.get_pos()
                    for row in keyboard:
                        for obj in row:
                            key = obj.get_key_at_pos(pos)
                    if key:
                        found = False
                        for x, row in enumerate(typed):
                            for y, element in enumerate(row):
                                if element is None:
                                    if x == guess_number:
                                        typed[x][y] = key.capitalize()
                                    found = True
                                    break
                            if found:
                                break
    
        update_board()
        update_keyboard()
        
        pygame.display.flip()


main()

    


