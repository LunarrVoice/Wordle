import word_lists
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode(WIDTH, HEIGHT)
pygame.display.set_caption("Wordle")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (30, 30, 30)

solution = random.choice(word_lists.SOLUTION_LIST)

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
    
    for guess in range(6):
        if level_over:
            break
        else:
            while True:
                user_input = check(guess())
            
                if user_input == "invalid":
                    continue
                else:
                    if sol_check(user_input) == "win":
                        print(f"You won in {guess + 1} guesses!")
                        level_over = True
                    else:
                        print(sol_check(user_input))

                    break


def main():
    while True:
        SCREEN.fill(BACKGROUND)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        level()


main()

    


