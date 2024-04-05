import word_lists
import random

solution = random.choice(word_lists.WORD_LIST)


def guess():
    guess_input = input("guess a 5 letter word: ")
    return guess_input


def check(guess_input):
    if len(guess_input) != 5:
        print("that word is not 5 letters long, try again")
        return "invalid"

    for word in range(len(word_lists.WORD_LIST)):
        if guess_input == word_lists.WORD_LIST[word]:
            print("Valid word")
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
    
    return letters


for x in range(6):
    while True:
        user_input = check(guess())
        if user_input == "invalid":
            continue
        else:
            print(sol_check(user_input))
            break



