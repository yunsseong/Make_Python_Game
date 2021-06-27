#지뢰찾기 게임
import random
import copy
import sys
#Generating Map

def print_mine_map_debug():
    for i in range(size_of_map):
        print(" ".join(map(str,mine_map_show[i])) + "    " + " ".join(map(str, (mine_map_sol[i]))))

def print_mine_map(map_obj):
    for i in map_obj:
        for j in i:
            print(j, end=" ")
        print("")
        
def mine_map_property():
    global size_of_map 
    #size_of_map = int(input("Input size of map : "))
    size_of_map = 10
    global num_of_mine 
    #num_of_mine = int(input("Input number of mine : ")) 
    num_of_mine = 10

def empty_mine_map_gen():
    map_horiz = []
    empty_mine_map = []
    for i in range(size_of_map):
        for j in range(size_of_map):
            map_horiz.append("#")
        empty_mine_map.append(map_horiz)
        map_horiz = []
    return empty_mine_map

def plant_mine_on_map(mine_planted_map):
    cord =[]
    flag_raised_map = copy.deepcopy(mine_planted_map)
    range_sizeOfMap = range(size_of_map)
    for i in range_sizeOfMap:
        for j in range_sizeOfMap:
            cord.append([i, j])
    ran_mine = random.sample(cord, num_of_mine)
    for i in ran_mine:
        mine_planted_map[i[0]][i[1]] = "*"
        flag_raised_map[i[0]][i[1]] = "^"
    return mine_planted_map, ran_mine, flag_raised_map


def make_mine_map_sol(mine_map_sol):
    cnt = 0  
    for i in range(size_of_map):
        for j in range(size_of_map):
            if mine_map_sol[i][j] != "*":
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        if i+a >= 0 and j+b >= 0 and i+a < size_of_map and j+b < size_of_map and abs(a)+abs(b)!=0:
                            if mine_map_sol[i+a][j+b] == "*":
                                cnt +=1
                mine_map_sol[i][j]=cnt
                cnt=0
    return mine_map_sol

        
def MAP_GEN():
    mine_map_property()
    empty_mine_map = empty_mine_map_gen()
    mine_planted_map, ran_mine, flag_raised_map = plant_mine_on_map(empty_mine_map)
    mine_map_sol = make_mine_map_sol(mine_planted_map)
    mine_map_show = empty_mine_map_gen()
    return mine_map_show, mine_map_sol, ran_mine, flag_raised_map

def game_end():
    print("You dig the mine, Game Over : ")
    MAIN_MENU()
    #MAIN_MENU()  
def game_end_happy():
    print("You saved many lives, Well done")
    MAIN_MENU()

def game_end_forgive():
    print("We still have Mines to dig... So come back ASAP ")
    MAIN_MENU()
        
def zero(y, x):
    cord_zero = []
    for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if y+a >= 0 and x+b >= 0 and y+a < size_of_map and x+b < size_of_map:
                    if mine_map_sol[y+a][x+b] == 0:
                        cord_zero.append([y+a,x+b])
                        mine_map_show[y+a][x+b] = mine_map_sol[y+a][x+b]
                    else:
                        mine_map_show[y+a][x+b] = mine_map_sol[y+a][x+b]
    for y,x in cord_zero:
        zero(y,x)

def dig_zero(y, x):
    for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if y+a >= 0 and x+b >= 0 and y+a < size_of_map and x+b < size_of_map:
                    mine_map_show[y+a][x+b] = mine_map_sol[y+a][x+b]

def zero(y, x):
    for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if y+a >= 0 and x+b >= 0 and y+a < size_of_map and x+b < size_of_map:
                    if mine_map_sol[y+a][x+b] == 0:
                        dig_zero(y+a, x+b)
                    else:
                        mine_map_show[y+a][x+b] = mine_map_sol[y+a][x+b]


# def frist_dig():
#     y, x = map(int, input("You should frist digging x, y : ").split())
#     y, x = y-1, x-1
#     for a in [-1, 0, 1]:
#         cord_zero = []
#             for b in [-1, 0, 1]:
#                 if y+a >= 0 and x+b >= 0 and y+a < size_of_map and x+b < size_of_map:
#                     if mine_map_sol[y+a][x+b] != "*" and mine_map_sol[y+a][x+b] == 0:
#                         mine_map_show[y+a][x+b] = mine_map_sol[y+a][x+b] 
#                         cord_zero.append([y+a,x+b])
#                     elif mine_map_sol[y+a][x+b] != "*":
#                         mine_map_show[y+a][x+b] = mine_map_sol[y+a][x+b] 
                        
def dig(y, x):
    if mine_map_sol[y][x] == "*":
        print_mine_map(mine_map_sol)
        game_end()
    elif mine_map_sol[y][x] == 0:
        zero(y,x)
        print_mine_map_debug()
        ask_command()
    else:
        mine_map_show[y][x] = mine_map_sol[y][x]
        print_mine_map_debug()
        ask_command()
        
def flag(y,x):
    if mine_map_show[y][x] in [1,2,3,4,5,6,7,8]:
        print("Error : You can't raise flag here")
        ask_command()
    elif mine_map_show[y][x] == "^":
        mine_map_show[y][x] == "#"
    else:
        mine_map_show[y][x] = "^"
        print_mine_map_debug()   
        ask_command()
    
def ask_command():
    user_commend = input("Dig(D) Flag(F) End(E) Check(C) : ").split()
    if user_commend[0] in ["d", "D", "dig", "f", "F", "flag", "c", "C", "check"]:
            if len(user_commend) == 3 and user_commend[0] not in ["e", "E"]:
                com, x, y = [user_commend[0], int(user_commend[1])-1, int(user_commend[2])-1]
                func_num = {"flag" : 1, "f": 1,"F": 1, "d": 0,"D": 0, "dig" : 0}.get(com)
                act_fun = func[func_num](y,x)
                act_fun()
            elif len(user_commend) == 1 and user_commend[0] in ["c","C", "check"]:
                check()
            else:
                print("Error : You have to input x, y collectly")
                ask_command()    
    elif user_commend[0] in ["e","E"]:
        game_end_forgive()
    else:
        print("Error : There is no such option")
        ask_command()      

def check():
    cnt = 0
    for i in mine_map_show:
        for j in i:
            if j == "^":
                cnt+=1
    if cnt == num_of_mine:
        for i in ran_mine:
            if mine_map_show[i[0]][i[1]] != "^":
                print("Oops.. You raise flage on the wrong places, Try again")
                ask_command()
            else:               
                game_end_happy()
        
    elif cnt < num_of_mine:
        print("Oops.. You still have mine to dig")
        ask_command()
    else:
        print("Oops.. You raise flag more than mine")
        ask_command()
        
def MAIN_MENU():
    user_dicision = input("Play(P) Setting(S) Exit(E) : ")
    if user_dicision in ["P", "p"]:
        print("Welcome to mine clearing squad, Your mission is find Mine and Save lives. Good luck!")
        mine_map_show, mine_map_sol, mine_cord, flag_raised_map = MAP_GEN()
        PLAY(mine_map_show, mine_map_sol, mine_cord, flag_raised_map)
    elif user_dicision in ["S", "s"]:
        MAIN_MENU()
    elif user_dicision in ["E", "e"]:
        print("Okay, See you later Captine")
        sys.exit()
    else:
        print("Error : There is no such option")
        MAIN_MENU()
        
def START():
    print("Dig Mines And Save Lives")
    MAIN_MENU()

def MAIN_MENU_DEBUG():
    mine_map_show, mine_map_sol, mine_cord = MAP_GEN()
    PLAY(mine_map_show, mine_map_sol, mine_cord)

def PLAY(mine_map_show_p, mine_map_sol_p, ran_mine_p, flag_raised_map_p):
    global mine_map_show, mine_map_sol, ran_mine ,flag_raised_map
    global func
    func = [dig, flag]
    mine_map_show, mine_map_sol, ran_mine,flag_raised_map = mine_map_show_p, mine_map_sol_p, ran_mine_p, flag_raised_map_p
    #print_mine_map_debug()
    #frist_dig()
    print_mine_map_debug()
    ask_command()
        
START()





        

