import numpy as np
import random
import read_map as rm
import matplotlib.pyplot as plt
'''
markov_reward - calculates markov reward for an input map
                requires map, reward_dictionary, move_probability, and a goal goal_position

choose_route_look_ahead - calculates a route using a markov previous_plan
                          requires a map, plan, start spot, and terminal states (just set to goal)
'''
def markov_reward(map_arr,reward_dict,move_prob, goal_position, previous_values = 'empty',extra_val = -1000):
    wrong_direc = move_prob
    movement = reward_dict['movement']
    if previous_values == 'empty':
        previous_values = create_zero_initial_values(map_arr,extra_val)
    new_values = np.copy(previous_values).tolist()
    i_row = map_arr.shape[0]
    i_col = map_arr.shape[1]
    for n_row in range(i_row):
        for n_col in range(i_col):
            current_val = 0

            if previous_values[n_row][n_col] != extra_val:
                current_val = previous_values[n_row][n_col] + movement
                #can add more in here for checking more areas
                for position in [[n_row,n_col]]:
                    if map_arr[position[0]][position[1]] == 0:

                        current_val += reward_on_spot(position,map_arr,reward_dict,goal_position,move_prob,previous_values)
                new_values[n_row][n_col] = current_val


    return new_values

def create_zero_initial_values(map_arr,extra_val):
    i_row = map_arr.shape[0]
    i_col = map_arr.shape[1]
    initial_values_array = np.empty(map_arr.shape, dtype='float')
    for n_row in range(i_row):
        for n_col in range(i_col):
            if map_arr[n_row][n_col] == 0:
                initial_values_array[n_row][n_col] = 0
            else:
                initial_values_array[n_row][n_col] = extra_val
    return initial_values_array


def reward_on_spot(position,map_arr,reward_dict,goal_position,move_prob,previous_plan):
    hit_wall = reward_dict['hit_wall']
    reached_goal = reward_dict['reached_goal']
    n_row = position[0]
    n_col = position[1]
    move_prob
    current_val = 0
    surrounding_cell = 0
    #check up
    if map_arr[n_row-1][n_col] == 1:
        current_val += hit_wall*move_prob
    elif map_arr[n_row-1][n_col] == 0:
        current_val += previous_plan[n_row-1][n_col]*move_prob
        surrounding_cell += 1

    #check down
    if map_arr[n_row+1][n_col] == 1:
        current_val += hit_wall*move_prob
    elif map_arr[n_row+1][n_col] == 0:
        current_val += previous_plan[n_row+1][n_col]*move_prob
        surrounding_cell += 1

    #check left
    if map_arr[n_row][n_col-1] == 1:
        current_val += hit_wall*move_prob
    elif map_arr[n_row][n_col-1] == 0:
        current_val += previous_plan[n_row][n_col-1]*move_prob
        surrounding_cell += 1

    #check right

    if map_arr[n_row][n_col+1] == 1:
        current_val += hit_wall*move_prob
    elif map_arr[n_row][n_col+1] == 0:
        current_val += previous_plan[n_row][n_col+1]*move_prob
        surrounding_cell += 1

    #goal
    if [n_row-1,n_col] == goal_position or [n_row+1,n_col] == goal_position or [n_row,n_col-1] == goal_position or [n_row,n_col+1] == goal_position:
        current_val += reached_goal*move_prob
    elif [n_row,n_col] == goal_position:
        current_val += reached_goal
    current_val = current_val/surrounding_cell
    return current_val

def choose_route(map_arr,plan,start_spot,terminal_states):
    at_terminal = False
    position = start_spot
    row_number = map_arr.shape[0]
    col_number = map_arr.shape[1]
    route = [position]
    while at_terminal == False:
        surrounding = [[position[0]-1,position[1]], [position[0]+1,position[1]], [position[0],position[1]-1], [position[0],position[1]+1]]
        for i in range(len(surrounding)-1,-1,-1):
            if surrounding[i][0] == row_number or surrounding[i][1] == col_number or surrounding[i][0] == 0 or surrounding[i][1] == 0 or map_arr[surrounding[i][0]][surrounding[i][1]] != 0 or surrounding[i] in route:
                surrounding.pop(i)
        weight_list = []
        for i_poss in surrounding:
            weight_list.append(plan[i_poss[0]][i_poss[1]])


        route.append(surrounding[weight_list.index(max(weight_list))])
        position = route[-1]
        print(position)


        if route[-1] in terminal_states:
            at_terminal = True

    return route


def choose_route_look_ahead(map_arr,plan,start_spot,terminal_states):
    at_terminal = False
    position = start_spot
    row_number = map_arr.shape[0]
    col_number = map_arr.shape[1]
    route = [position]
    while at_terminal == False:
        surrounding = [[position[0]-1,position[1]], [position[0]+1,position[1]], [position[0],position[1]-1], [position[0],position[1]+1]]
        for i in range(len(surrounding)-1,-1,-1):
            if surrounding[i][0] == row_number or surrounding[i][1] == col_number or surrounding[i][0] == 0 or surrounding[i][1] == 0 or map_arr[surrounding[i][0]][surrounding[i][1]] != 0 or surrounding[i] in route:
                surrounding.pop(i)
        weight_list = []
        surr_len = len(surrounding)
        for i_poss in surrounding:
            weight_list.append(plan[i_poss[0]][i_poss[1]])
            for pos_iter in [[i_poss[0]-1,i_poss[1]],[i_poss[0]+1,i_poss[1]],[i_poss[0],i_poss[1]-1],[i_poss[0],i_poss[1]+1]]:
                if map_arr[pos_iter[0],pos_iter[1]] == 0:

                    weight_list[len(weight_list)-1] += plan[pos_iter[0]][pos_iter[1]]

        try:
            route.append(surrounding[weight_list.index(max(weight_list))])
        except:

            print('bad path')
            return route
        position = route[-1]



        if route[-1] in terminal_states:
            
            at_terminal = True


    return route
