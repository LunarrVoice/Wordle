import word_lists
import random

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

game_over = False

for x in range(6):
    if game_over:
        break
    else:
        while True:
            user_input = check(guess())
            
            if user_input == "invalid":
                continue
            else:
                if sol_check(user_input) == "win":
                    print(f"You won in {x + 1} guesses!")
                    game_over = True
                else:
                    print(sol_check(user_input))

                break



