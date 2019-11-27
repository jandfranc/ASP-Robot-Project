import numpy as np
import markov_decision as md
from PIL import Image

def map_read_skimage(map):
    map_arr = imread(map)
    result = map_arr[:, :, 0]
    for i_height in range(0,result.shape[0]):
        for i_width in range(0,result.shape[1]):
            if result[i_height][i_width] < 100:
                result[i_height][i_width] = 0
            elif result[i_height][i_width] >225:
                result [i_height][i_width] = 1
            else:
                result[i_height][i_width] = 2
    return result

def map_read(map):
    map_arr = np.asarray(Image.open(map))
    result = np.copy(map_arr[:, :, 0])
    for i_height in range(0,result.shape[0]):
        for i_width in range(0,result.shape[1]):
            if result[i_height][i_width] < 100:
                result[i_height][i_width] = 1
            elif result[i_height][i_width] >225:
                result [i_height][i_width] = 0
            else:
                result[i_height][i_width] = 2
    return result

def find_rooms_and_doors(map_arr):
    row_number = map_arr.shape[0]
    col_number = map_arr.shape[1]
    i = 0
    room_list = []
    for i_row in range(0,row_number-1):
        for i_col in range(0,col_number-1):
            if map_arr[i_row][i_col] == 1 and map_arr[i_row+1][i_col] == 1 and map_arr[i_row][i_col+1] == 1 and map_arr[i_row+1][i_col+1] == 0:
                top_corner = [i_row,i_col]
                r_row = i_row+1
                r_col = i_col+1
                while map_arr[r_row+1][r_col] != 1:
                    r_row += 1
                while map_arr[r_row][r_col+1] != 1:
                    r_col+=1
                bottom_corner = [r_row+1,r_col+1]

                room_list.append([top_corner,bottom_corner])
    ver_doors = []
    hor_doors = []
    for room in room_list:
        room_height = room[1][0] - room[0][0]
        room_width = room[1][1] - room[0][1]
        #check top and bottom
        sides = -1

        for v_side in range(0,2):
            found_door = False
            wall = room[v_side][0] + sides
            for room_col in range(0,room_width):

                other_wall = room_col + room[0][1]


                if found_door == False and map_arr[wall, other_wall] == 0:
                    found_door = True
                    door_start = [wall, other_wall]

                if found_door == True and map_arr[wall, other_wall] == 1:
                    door_end = [wall, other_wall -1]
                    hor_doors.append([door_start,door_end,room])
                    found_door = False
                    #print(room_width)
                    door_start= None
                    door_end = None
                    #print(map_arr[wall, room_col])
                    #print(hor_doors)

            sides = 1



    return room_list, hor_doors


def create_room_arr(room_list,hor_doors,map_arr):
    rooms = []
    room_num = 0
    for room in room_list:
        rooms.append(Room(room,room_list,hor_doors,map_arr,room_num))
        room_num += 1
    return rooms

class Room():
    def __init__(self,room,room_list,doors,map_arr,room_num):
        self.room = room
        self.global_doors = doors
        self.map_arr = map_arr
        self.room_num = room_num
        self.room_list = room_list
        self.goal = None
        self.reward_dict = {'hit_wall':-100,'movement':-1,'reached_goal':100000}
        self.room_map()
        self.find_connections()
        self.find_goals()
        self.ASP_connections()
        self.make_init_plans()



    def room_map(self):
        self.roombox = np.copy(self.map_arr[self.room[0][0]:self.room[1][0]+1,self.room[0][1]:self.room[1][1]+1])
        self.roombox = np.pad(self.roombox, [(1, 1), (1, 1)], mode='constant', constant_values=1)

    def find_connections(self):
        diff_doors = []
        self.same_doors = []
        for door in self.global_doors:
            if door[2] != self.room:
                diff_doors.append(door)
            else:
                self.same_doors.append(door)

        self.connections = []
        self.door_connect = []
        for same in self.same_doors:
            for diff in diff_doors:
                if (abs(same[0][0]-diff[0][0]) < 10) and same[0][1] == diff[0][1]:
                    self.connections.append([diff[2],same[0:2]])
                    self.door_connect.append([diff[0:2],same[0:2]])

    def find_goals(self):
        self.local_doors = []
        for door in self.global_doors:
            if door[2] == self.room:
                loc_door_x1 = door[0][0]-door[2][0][0]+1
                loc_door_x2 = door[1][0]-door[2][0][0]+1
                loc_door_y1 = door[0][1]-door[2][0][1]+1
                loc_door_y2 = door[1][1]-door[2][0][1]+1

                self.local_doors.append([[loc_door_x1,loc_door_y1],[loc_door_x2,loc_door_y2], door])

        self.goals = []

        for loc_door in self.local_doors:
            goal_x = loc_door[0][0] + int((loc_door[1][0]-loc_door[0][0])/2)
            goal_y = loc_door[0][1] + int((loc_door[1][1]-loc_door[0][1])/2)

            if goal_x == self.roombox.shape[0]-1:
                goal_x += -1
            elif goal_x == 0:
                goal_x += 1
            if goal_y == self.roombox.shape[1]-1:
                goal_y += -1
            elif goal_y == 0:
                goal_y += 1
            self.goals.append([[goal_x,goal_y],loc_door[0:2]])


    def ASP_connections(self):
        self.ASP_connect = []
        for connect in self.connections:
            val = self.room_list.index(connect[0])
            self.ASP_connect.append(f'holds(adjacent(x{self.room_num}, x{val}),0).')

    def make_init_plans(self):
        self.markov_plans = []

        for goal in self.goals:

            it_markov_reward = md.markov_reward(self.roombox,self.reward_dict,0.7,goal[0])

            for i in range(0,5):
                it_markov_reward = md.markov_reward(self.roombox,self.reward_dict,1,goal[0], it_markov_reward)
            self.markov_plans.append([it_markov_reward, goal])


    def start_point_calc(self,start_point):
        start_x = start_point[0] - self.room[0][0]+1
        start_y = start_point[1] - self.room[0][1]+1
        return [start_x,start_y]

    def convert_route_global(self,point):
        start_x = point[0] + self.room[0][0]-1
        start_y = point[1] + self.room[0][1]-1
        return [start_x,start_y]

def create_asp(room_obj_list):
    asp_list = []
    for room in room_obj_list:
        for bap in room.ASP_connect:
            asp_list.append(bap)
    return asp_list
