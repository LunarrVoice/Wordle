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

solution = random.choice(word_lists.SOLUTION_LIST)

board = []
typed = []

class Square:
    def __init__(self, name, x, y, has_text=False):
        self.name = name
        self.x = (50 * x) + (30 * x) + 125
        self.y = (50 * y) + (30 * y) - 50
        self.has_text = has_text
        
    def draw_square(self):
        pygame.draw.rect(SCREEN, LIGHTGREY, (self.x - 1, self.y - 1, 72, 72))
        pygame.draw.rect(SCREEN, BACKGROUND, (self.x, self.y, 70, 70))
        
    def draw_text(self, text):
        draw_text(SCREEN, text, WHITE, self.x + 35, self.y + 35, 44)
        
     
def init_board(letters, guesses):
    global board, typed
    
    board = [[None for x in range(letters)] for x in range(guesses)]
    
    for letter in range(letters):
        for guess in range(guesses):
            object_name = f"square{letter + 1}{guess + 1}"
            board[guess][letter] = Square(object_name, letter + 1, guess + 1)
            
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
    

def guess():
    guess_input = input("guess a 5 letter word: ")
    return guess_input


def check(guess_input):
    if len(guess_input) != 5:
        print("that word is not 5 letters long, try again")
        return "invalid"

    with open("words.txt", "r") as file:
        for line in file:
            if guess_input in line:
                return guess_input

    print("That word is not valid")
    return "invalid"


def sol_check(guess_input):
    letters = ["", "", "", "", ""]

    for x in range(5):
        if solution[x] == guess_input[x]:
            letters[x] = "green"

    for x in range(5):
        for y in range(5):
            if solution[y] == guess_input[x]:
                if letters[x] == "":
                    letters[x] = "yellow"
                    break
                elif letters[x] == "green":
                    break

    if letters == ["green", "green", "green", "green", "green"]:
        return "win"
    
    return letters


def level():
    level_over = False
    
    for x in range(6):
        if level_over:
            break
        else:
            while True:
                user_input = check(guess())
            
                if user_input == "invalid":
                    continue
                else:
                    if sol_check(user_input) == "win":
                        print(f"You won in {x + 1} guesses!")
                        level_over = True
                    else:
                        print(sol_check(user_input))

                    break


def main():
    global board, typed
    
    typed = [[None for x in range(5)] for x in range(6)]
    
    while True:
        SCREEN.fill(BACKGROUND)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    continue
                else:
                    found = False
                    for x, row in enumerate(typed):
                        for y, element in enumerate(row):
                            if element is None:
                                typed[x][y] = event.unicode.capitalize()
                                found = True
                                break
                        if found:
                            break
        
        init_board(5, 6)
        
        pygame.display.flip()


main()

    


