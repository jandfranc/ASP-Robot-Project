import markov_decision as md
import read_map as rm
import utilASP as ua
import matplotlib.pyplot as plt
import numpy as np
import pickle

def run_experiment(start_room,start_point,init_goal,goal_point,reward_dict,move_prob,discount,iterations,map,map_no_obstacle):
    map_arr = rm.map_read(map)
    map_arr_no_obs = rm.map_read(map_no_obstacle)

    room_list, doors = rm.find_rooms_and_doors(map_arr_no_obs)

    rooms = rm.create_room_arr(room_list,doors,map_arr,reward_dict,move_prob,discount,iterations)

    asp_rooms = rm.create_asp(rooms)



    asp_doc = ua.read_file_sp_to_list('grid_move_template.sp')

    constants_list, sorts_list, predicates_list, rules_list, display_list = ua.split_asp_sections(asp_doc)

    rules_list = ua.add_rules(rules_list,asp_rooms)


    rules_list = ua.add_rules(rules_list,[f'holds(at(r,x{start_room}),0).',f'goal(I) :- holds(at(r,x{init_goal}),I).'])

    if start_room != init_goal:
        new_asp_doc = ua.add_sections_together(constants_list, sorts_list, predicates_list, rules_list, display_list)

        ua.write_list_to_file('first_test.sp',new_asp_doc)

        min_route = ua.find_minimal_answersets('first_test.sp','temp.sp', len(rooms))



        asp_route = [start_room]
        if min_route != False:
            for item in min_route[0]:
                asp_route.append(int(item[15]))
    else:
        asp_route = start_room
    if min_route != False:
        route = []
        for it in range(0,len(asp_route)):

            if asp_route[it] == asp_route[0] and len(asp_route) != 1:


                curr_goal = rooms[asp_route[it]].markov_plans[0][1][0]
                loc_route = md.choose_route_look_ahead(rooms[asp_route[it]].roombox,rooms[asp_route[it]].markov_plans[0][0],rooms[asp_route[it]].start_point_calc(start_point),[curr_goal])
                global_route = []

                for loc_point in loc_route:
                    global_route.append(rooms[asp_route[it]].convert_route_global(loc_point))
                route = route + global_route
            elif len(asp_route)==1:
                goal_point_loc = room[route[it]].start_point_calc(goal_point)
                iteration = 0
                plan_same = md.markov_reward(rooms[asp_route[it]].roombox,rooms[asp_route[it]].reward_dict,move_prob, goal_point_loc, 'empty',-100, discount, iteration)
                iteration += 1
                for plan_iter in range(0,iterations-1):
                    plan_same = md.markov_reward(rooms[asp_route[it]].roombox,rooms[asp_route[it]].reward_dict,move_prob, goal_point_loc,plan_same,-100, discount, iteration)
                    iteration += 1
                loc_route = md.choose_route_look_ahead(rooms[asp_route[it]].roombox,plan_same,start_point,[goal_point])
                global_route = []
                for loc_point in loc_route:
                    global_route.append(rooms[asp_route[it]].convert_route_global(loc_point))
                route = route + global_route

            elif it == len(asp_route)-1:
                prev_room = rooms[asp_route[it-1]].room
                for connect_room in rooms[asp_route[it]].connections:
                    if prev_room == connect_room[0]:
                        prev_door = connect_room[1]
                for loc_door in rooms[asp_route[it]].local_doors:
                    if loc_door[2][0:2] == prev_door:
                        for it_goal in rooms[asp_route[it]].goals:
                            if it_goal[1] == loc_door[0:2]:
                                next_start = it_goal[0]

                goal_point_loc = rooms[asp_route[it]].start_point_calc(goal_point)
                iteration = 0
                plan_same = md.markov_reward(rooms[asp_route[it]].roombox,rooms[asp_route[it]].reward_dict,move_prob, goal_point_loc, 'empty', -100, discount, iteration)
                iteration += 1
                for plan_iter in range(0,iterations-1):
                    plan_same = md.markov_reward(rooms[asp_route[it]].roombox,rooms[asp_route[it]].reward_dict,move_prob, goal_point_loc, plan_same, -100, discount, iteration)
                    iteration +=1
                loc_route = md.choose_route_look_ahead(rooms[asp_route[it]].roombox,plan_same,next_start,[goal_point_loc])
                global_route = []
                for loc_point in loc_route:
                    global_route.append(rooms[asp_route[it]].convert_route_global(loc_point))
                route = route + global_route

            else:
                prev_room = rooms[asp_route[it-1]].room
                next_room = rooms[asp_route[it+1]].room
                for connect_room in rooms[asp_route[it]].connections:
                    if prev_room == connect_room[0]:
                        prev_door = connect_room[1]
                    if next_room == connect_room[0]:
                        next_door = connect_room[1]


                for loc_door in rooms[asp_route[it]].local_doors:
                    if loc_door[2][0:2] == prev_door:
                        for it_goal in rooms[asp_route[it]].goals:
                            if it_goal[1] == loc_door[0:2]:

                                next_start = it_goal[0]

                    if loc_door[2][0:2] == next_door:
                        for it_goal in rooms[asp_route[it]].goals:
                            if it_goal[1] == loc_door[0:2]:

                                next_goal = it_goal[0]


                for plan in rooms[asp_route[it]].markov_plans:


                    if next_goal == plan[1][0]:

                        curr_plan = plan

                loc_route = md.choose_route_look_ahead(rooms[asp_route[it]].roombox,curr_plan[0],next_start,[next_goal])
                #print(loc_route)
                #print(next_start)
                #print(next_goal)
                global_route = []
                for loc_point in loc_route:
                    global_route.append(rooms[asp_route[it]].convert_route_global(loc_point))
                route = route + global_route
    return route, map_arr, rooms

def save_map(map_arr,route):
    global start_point
    global goal_point
    global reward_dict
    global move_prob
    global discount
    global iterations
    hit_wall = reward_dict['hit_wall']
    reached_goal = reward_dict['reached_goal']
    map_arr_r = np.copy(map_arr)
    i = 5
    for pos in route[1::]:
        map_arr_r[pos[0],pos[1]] = 3
        i += 1
    map_arr_r[start_point[0],start_point[1]] = 5
    map_arr_r[goal_point[0],goal_point[1]] = 5

    with open(f'plans/move_prob{move_prob}_discount{discount}_iterations{iterations}_hitwall{hit_wall}_reachedgoal{reached_goal}.txt', "w") as text_file:
        for part in route:
            text_file.write(str(part))

    plt.figure()
    #plt.imshow(rooms[0].markov_plans[0][0])
    plt.imshow(map_arr_r)
    plt.savefig(f'plans/move_prob{move_prob}_discount{discount}_iterations{iterations}_hitwall{hit_wall}_reachedgoal{reached_goal}.png')

if __name__ == '__main__':
    start_room = 0
    start_point = [18,18]
    init_goal = 5
    goal_point = [85,10]


    # reward_dict = {'hit_wall':10,'reached_goal':100}
    # move_prob = 0.9
    # discount = 0.9
    # iterations = 50

    map = 'maps/experiment_obs.png'
    map_no_obstacle = 'maps/experiment_no_obs.png'

    hit_wall_list = [-100,-10,0]
    reached_goal_list = [10,100,1000]
    move_prob_list = [0.3,0.8,1]
    discount_list = [0.5,0.9,1]
    iterations = 50
    for hw in hit_wall_list:
        for rg in reached_goal_list:
            for mp in move_prob_list:
                for dis in discount_list:
                    reward_dict = {'hit_wall':hw,'reached_goal':rg}
                    move_prob = mp
                    discount = dis
                    route, map_arr, rooms = run_experiment(start_room,start_point,init_goal,goal_point,reward_dict,move_prob,discount,iterations,map,map_no_obstacle)
                    save_map(map_arr,route)

else:
    print('no route found')
