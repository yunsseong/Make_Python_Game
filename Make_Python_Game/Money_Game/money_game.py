import random
import sys

global user_coin

def main_menu():
    global user_coin
    user_coin = 100
    print("$$ Welcom to Money Game $$")
    user_input = input("Wanna play some game? (Y/N) : ").lower()
    if user_input in ["y", "yes"]:
        main_game_process()
    elif user_input in ["n", "no"]:
        print("Your choice is good")
        sys.exit()
    else:
        print("We only have two optins Yes Or No, Do you understand?")
        main_menu()

def main_game_process():
    global user_coin
    print("$$---------------------------------------$$")
    print("You have ", user_coin, "coin(s), Insert the coins you want :")
    bet_coin=input()
    if bet_coin.isdigit():
        bet_coin=int(bet_coin)
        your_luck=random.randrange(1,101)
        if user_coin >= bet_coin:
            if your_luck > 50:
                print("Oh you are lucky, Take your money")
                user_coin += bet_coin *2
            else:
                print("Oops This time was unlucky")
                user_coin -= bet_coin *2
            user_coin_check()
        else:
            print("HAHA Gotcha, How dare you cheet!")
            main_game_process()
    else:
        print("Hmm We only get number, Try again")
        main_game_process()

def user_coin_check():
    global user_coin
    if user_coin <= 0:
        print("GAME OVER")
        main_menu()
    else:
        main_game_process()

main_menu()