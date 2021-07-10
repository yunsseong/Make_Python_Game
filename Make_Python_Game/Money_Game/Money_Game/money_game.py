import random
import sys

global user_coin
user_coin = 100

def main_menu():
    print("$$ Welcom to Money Game $$")
    user_input = input("Wanna play some game? (Y/N) : ").lower()
    if user_input in ["y", "yes"]:
        main_game_process()
    elif user_input in ["n", "no"]:
        print("Your choice is good")
        sys.exit()
    else:
        print("Hmm... You choice wrong option, Try again")
        main_menu()

def main_game_process():
    global user_coin
    print("$$---------------------------------------$$")
    print("You have ", user_coin, "coin(s), Insert the coins you want :")
    bet_coin=int(input())
    your_luck=random.randrange(1,101)
    if your_luck > 50:
        print("Oh you are lucky, Take your money")
        user_coin += bet_coin *2
    else:
        print("Oops This time was unlucky")
        user_coin -= bet_coin *2
    user_coin_check()

def user_coin_check():
    if user_coin <= 0:
        print("GAME OVER")
        main_menu()
    else:
        main_game_process()

main_menu()