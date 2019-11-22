import numpy as np
import random

def create_grid(size = [5,5]):
#creates grid of a given size in asp logic
    i_row = size[0]
    i_col = size[1]
    i = -1
    array = np.empty(size, dtype='object')

    grid_asp = []

    for n_row in range(i_row):
        for n_col in range(i_col):
            i+=1
            array[n_row][n_col] = f'x{i}'

    for n_row in range(i_row):
        for n_col in range(i_col):
            if n_row == 0 and n_col == 0:
              grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row+1,n_col]}),0).')
              grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col+1]}),0).')

            elif n_row == 0 and n_col == i_col-1:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row+1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col-1]}),0).')

            elif n_row == i_row-1 and n_col == 0:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row-1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col+1]}),0).')

            elif n_row == i_row-1 and n_col == i_col-1:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row-1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col-1]}),0).')

            elif n_row == 0:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row+1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col+1]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col-1]}),0).')

            elif n_col == 0:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row+1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col+1]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row-1,n_col]}),0).')

            elif n_row == i_row-1:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row-1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col+1]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col-1]}),0).')

            elif n_col == i_col-1:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row+1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col-1]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row-1,n_col]}),0).')

            else:
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row+1,n_col]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col+1]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row,n_col-1]}),0).')
                grid_asp.append(f'holds(adjacent({array[n_row,n_col]}, {array[n_row-1,n_col]}),0).')
    return grid_asp



def actor_location(grid_size,actors):
#assigns random initial location to actors - used later for goals and subgoals
    actor_loc = []
    for it_actor in len(actors):
        check  = True
        while check:
            row = np.random.randint(grid_size[0])
            col = np.random.randint(grid_size[1])
            if [row,col] in actor_loc:
                continue
            else:
                actor_loc.append[row,col]
                check = False
    return actor_loc

def initial_people_object_pair(object_num):
#outputs people-object pairs in asp logic
    init_pairs_asp = []
    for it_object in range(0,object_num):
        init_pairs_asp.append(f'holds(has(p{it_object}, o{it_object}),0).')
    return init_pairs_asp

def random_goal_state(people_num,object_num):
    if people_num <= object_num:
        raise ValueError('people_num must be larger than object_num')
        return
    object_list = []
    people_list = []
    for it_object in range(0,object_num):
        object_list.append(it_object)

    for it_people in range(0,people_num):
        people_list.append(it_people)

    random.shuffle(object_list)
    random.shuffle(people_list)

    goal_list_ASP = []
    for it_rule in range(0,object_num):
        goal_list_ASP.append(f'holds(has(p{people_list.pop()}, o{object_list.pop()}),I).')

    return goal_list_ASP





if __name__ == '__main__':

    print(initial_people_object_pair(7))
    print(random_goal_state(9,7))
