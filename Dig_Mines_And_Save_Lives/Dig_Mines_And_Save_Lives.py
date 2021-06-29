#지뢰찾기 게임
import random
import copy
import sys
global GAME_MODE
GAME_MODE = "DEBUG"

#역할 : 맵을 터미널에 출력하는 함수
def print_map(*map_obj):
    if GAME_MODE == "NOMAL":
        for i in map_obj:
            for j in i:
                print(j, end = " ")
            print("")
    elif GAME_MODE == "DEBUG":
        for i in range(size_of_map):
            print(" ".join(map(str,mine_map_show[i])) + "    " + " ".join(map(str, (mine_map_sol[i]))))

#역할 : 정해진 타입만 받도록하는 함수
#추후 수정사항 : 여러개의 인수를 넣는 경우도 보호해야할 필요가 있음
def safe_int_input(print_str):
    input_tmp = input(print_str)
    if input_tmp.isdigit() == True:
        return int(input_tmp)
    else:
        print("Error : You should input digit number")
        safe_int_input(print_str)


#역할 : 디버그 모드일 경우 기본맵과 기본지뢰 갯수대로 맵 속성을 설정
def set_map_property():
    global size_of_map, num_of_mine
    if GAME_MODE == "NOMAL":
        print_str = "Input size of map : "
        size_of_map = safe_int_input(print_str)
        print_str = "Input number of mines : "
        num_of_mine = safe_int_input(print_str)
    elif GAME_MODE == "DEBUG":
        size_of_map, num_of_mine = 10,10
         
def MINE_MAP_GEN():
    #빈 지뢰 맵 생성
    set_map_property()
    map_horiz = []
    empty_mine_map = []
    for i in range(size_of_map):
        for j in range(size_of_map):
            map_horiz.append("#")
        empty_mine_map.append(map_horiz)
        map_horiz = []
    global mine_map_show, mine_planted_map
    mine_map_show = copy.deepcopy(empty_mine_map)
    mine_planted_map = copy.deepcopy(empty_mine_map)
    
    #빈 맵에 랜덤으로 지뢰를 심기
    cord =[]
    range_sizeOfMap = range(size_of_map)
    # 추후 수정사항 : 좌표 리스트 생성하는 부분 리스트 컴프리헨션으로 줄여보기
    for i in range_sizeOfMap:
        for j in range_sizeOfMap:
            cord.append([i, j])
    global ran_mine
    ran_mine = random.sample(cord, num_of_mine)
    for i in ran_mine:
        mine_planted_map[i[0]][i[1]] = "*"
    global mine_map_sol
    mine_map_sol = copy.deepcopy(mine_planted_map)
    
    #정답 맵 생성
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
                
#어떤 상황에서 게임이 끝났는지 결과 변수에 담아서 각 상황별로 분류해서 멘트 출력, 함수 단일화
def game_end(RES):
    Bad_ment = "You dig the mine, We will remember your sacrifice"
    Happy_ment = "You saved many lives, Well done"
    Forgive_ment = "We still have Mines to dig... So come back ASAP"
    print_str = {"BAD" : Bad_ment, "HAPPY" : Happy_ment, "FORGIVE" : Forgive_ment}.get(RES)
    print(print_str)
    MAIN_MENU()

#추후 수정 사항 : 0을 선택했을때 그 주변 0과 숫자를 알려주는 기능 추가, 처음 누르는 부분을 0으로 하고 이걸 기준으로 맵을 생성(이유 : 처음 클릭한 곳이 지뢰인 것을 방지하기 위해)
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
                        
def dig(y, x):
    if mine_map_sol[y][x] == "*":
        print_mine(mine_map_sol)
        game_end("BAD")
    elif mine_map_sol[y][x] == 0:
        zero(y,x)
        print_map(mine_map_show)
        ask_command()
    else:
        mine_map_show[y][x] = mine_map_sol[y][x]
        print_map(mine_map_show)
        ask_command()
        
def flag(y,x):
    if mine_map_show[y][x] in [1,2,3,4,5,6,7,8]:
        print("Error : You can't raise flag here")
        ask_command()
    elif mine_map_show[y][x] == "^":
        mine_map_show[y][x] == "#"
    else:
        mine_map_show[y][x] = "^"
        print_map(mine_map_show)   
        ask_command()

#역할 : 사전에 정해놓은 명령어 형식에 맞도록 입력을 제한하는 함수        
def safe_input_commend(num_params, print_str, params_type):
    input_tmp = input(print_str).split()
    if num_params == len(input_tmp):
        for i in range(num_params):
            if params_type[i] == "STR":
                if input_tmp[i].isalpha():
                    pass
                else:
                    print("Error : Your commend something wrong")
                    safe_input_commend(num_params, print_str, params_type)
            elif params_type[i] == "INT":
                if input_tmp[i].isdigit():
                    input_tmp[i] = int(input_tmp)
                else:
                    print("Error : Your commend something wrong")
                    safe_input_commend(num_params, print_str, params_type)
    else:
        print("Error : Something wrong in number of commend parameters")
        safe_input_commend(num_params, print_str, params_type)
    return input_tmp
                

# 추후 수정사항 : 입력받고 다 소문자로 변환할 것, 좌표값 입력받는 것도 자연수 값만 받도록 조정할 것  
def ask_command():
    user_commend = input("Dig(D) Flag(F) End(E) Check(C) : ").split()
    if user_commend[0] in ["d", "D", "dig", "f", "F", "flag", "c", "C", "check"]:
            if len(user_commend) == 3 and user_commend[0] not in ["e", "E"]:
                com, x, y = [user_commend[0], int(user_commend[1])-1, int(user_commend[2])-1]
                act_func = {"d": dig(y, x),"D": dig(y, x), "dig" : dig(y, x), "flag" : flag(y, x), "f": flag(y, x),"F": flag(y, x)}.get(com)
                act_fun(y, x)
            elif len(user_commend) == 1 and user_commend[0] in ["c","C", "check"]:
                check()
            else:
                print("Error : You have to input x, y collectly")
                ask_command()    
    elif user_commend[0] in ["e","E"]:
        game_end("FORGIVE")
    else:
        print("Error : There is no such option")
        ask_command()      

#추후 수정사항 : check는 한 턴이 끝날때 마다 자동으로 하다록 변경
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
                game_end("HAPPY")
        
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
        MINE_MAP_GEN()
        PLAY()
    elif user_dicision in ["S", "s"]:
        MAIN_MENU()
    elif user_dicision in ["E", "e"]:
        print("Okay, See you later Captine")
        sys.exit()
    elif user_dicision in ["DEBUG"]:
        GAME_MODE = "DEBUG"
        PLAY()
    else:
        print("Error : There is no such option")
        MAIN_MENU()
        
def START():
    print("Dig Mines And Save Lives")
    MAIN_MENU()


def PLAY():
    print_map(mine_map_show)
    ask_command()
        
START()





        

