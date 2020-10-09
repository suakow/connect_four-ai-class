import argparse
import time

debug = False
max_depth = 12
# is_white_turn = False
state = ([],[],[],[],[],[],[])

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--first', action='store_false')
parser.add_argument('-d', '--depth', action='store', dest='depth', default=4, type=int) 
args = parser.parse_args()

is_white_turn = args.first
set_depth = args.depth

def push(col,chip,state):
    if len(state[col]) >= 6:
        return False
    state[col].append(chip)

def check_window(state,chip,i,j):
    state = [s+['o']*(7-len(s)) for s in state]
    # print(state)
    max_count = 0
    count = 0
    if i <= 3:
        count = 0
        for col in range(4):
            if state[i+col][j] == chip:
                count += 1
            elif state[i+col][j] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
    if j >= 3:
        count = 0
        for row in range(4):
            if state[i][j-row] == chip:
                count += 1
            elif state[i][j-row] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count

    if i <= 3 and j >= 3:
        count = 0
        for k in range(4):
            if state[i+k][j-k] == chip:
                count += 1
            elif state[i+k][j-k] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
    
    if i <= 3 and j <= 2:
        count = 0
        for k in range(4):
            if state[i+k][j+k] == chip:
                count += 1
            elif state[i+k][j+k] != 'o':
                count = 0
                break
        if count == 4:
            return (i,j,4)
    if count > max_count:
        max_count = count
        
    # if max_count == 3 and (j == 0 or state[i][j-1] != 'o') and state[i][j] == 'o':
    #    return (i,j,3)
    # if max_count == 3 and state[i][j-1] == 'o':
    #    return (i,j,3)
    return (i,j,max_count)

def utility(state,chip):
    ret = is_win(state,chip)
    if debug: show_state(state)
    if debug: print(ret)
    if chip == 'B':
        return ret[2]
    return -ret[2]
    

def is_win(state,chip):
    max = -1
    for i in range(7):
        for j in range(6):
            ret=check_window(state,chip,i,j)
            if ret[2] > max:
                max = ret[2]
                ans = ret
    return ans

def show_state(state):
    state = [s+['o']*(7-len(s)) for s in state]
    for r in range(5,-1,-1):
        str_out = ''
        for c in range(7):
            str_out += state[c][r]
        print(str_out)
    print('1234567')
    # print(state)

def min_value_function(state,a,b,level):
    # just pushed black
    if is_win(state,'B')[2] == 4:
        return 4
    if level >= max_depth:
        if debug: print('Cutoff',state)
        ret_u = utility(state,'B')
        if debug: print('Utility',ret_u)
        return ret_u
    v=100
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'W',new_state)
        v = min(v,max_value_function(new_state,a,b,level+1))
        if v <= a:
            return v
        if b == 10:
            b = v
        else:
            b = min(b,v)
    return v

def max_value_function(state,a,b,level):
    # just pushed white
    if is_win(state,'W')[2] == 4:
        return -4
    v=-100
    # if black can win
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'B',new_state)
        if is_win(new_state,'B')[2] == 4:
            return 4
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'B',new_state)
        v = max(v,min_value_function(new_state,a,b,level+1))
        if v >= b:
            return v
        if a == -10:
            a = v
        else:
            a = max(a,v)
    return v

def alpha_beta_decision(state):
    global max_depth, set_depth
    s_res = sum([len(c) for c in list(state)])
    # First turn of computer -> 
    if s_res == 1 :
        ind = 0
        for c in list(state):
            if len(c) == 1:
                if ind == 0:
                    return 1
                else:
                    return ind-1
            ind += 1
    elif s_res == 0:
        return 3
    if s_res < 5:
        max_depth = set_depth
    elif s_res < 12:
        # max_depth = 6
        max_depth = set_depth
    elif s_res < 24:
        # max_depth = 8
        max_depth = set_depth
    else:
        # max_depth = 10
        max_depth = set_depth

    max_value = -100
    a,b=-10,10
    min_score=[]
    count_win = 0
    count_lose = 0
    for i in range(7):
        if len(state[i]) == 6:
            continue
        new_state = tuple([list(new_col) for new_col in state])
        push(i,'B',new_state)
        ret=min_value_function(new_state,a,b,0)
        min_score.append(ret)
        if debug: print('MiniMax Value',ret)
        if debug: show_state(new_state)
        if ret > max_value:
            max_value=ret
            action = i
        if ret == 4:
            count_win += 1
        elif ret == -4:
            count_lose += 1
    if count_win >= 1:
        print('From my calculation, I will win')
    elif count_lose == 7:
        print('From my calculation, you will win')
    print(min_score,action)
    return action
  
#state=[['B', 'B', 'B','W'], [], ['W', 'W','B'], ['B', 'W','B'], ['W','W'], ['W'], []]
show_state(state)
round = 1
while sum([len(c) for c in list(state)]) != 42:
    print('----- Round : %s ------'%(round))
    round += 1
    if is_white_turn:
        c = int(input('Please enter your column:'))
        while len(state[c-1]) == 6:
            print('You cannot put in column',c)
            c = int(input('Please enter your column:'))
        print('W Turn : %s'%(c))
        push(c-1,'W',state)
        if is_win(state,'W')[2] == 4:
            print('You win!!!')
            show_state(state)
            break
        is_white_turn = False
    else:
        cal_start_time = time.time()
        c = alpha_beta_decision(state)
        print('B Turn : %s'%(c+1))
        push(c,'B',state)
        show_state(state)
        print("*calculation time : %s seconds" % (time.time() - cal_start_time))
        if is_win(state,'B')[2] == 4:
            print('I win!!!')
            break
        is_white_turn = True

    print('is_win: W:', is_win(state,'W'))
    print('is_win: B:', is_win(state,'B'))
    print(state)