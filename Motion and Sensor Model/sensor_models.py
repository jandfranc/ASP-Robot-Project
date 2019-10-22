import numpy as np


def scan_model(measurements, pose, map):
    returned_value = 1
    z_hit = 1
    z_random = 1
    z_max = 3
    std_hit = 1
    x, y, theta = pose
    x_sens= 0
    y_sens = 0
    #THESE VARIABLES NEED TO BE TUNED
    theta_angle= np.radians(240/len(measurements))
    theta_sens = np.radians(-120)
    dist = 999999999999999999
    for i_measurement in range(0,len(measurements)):
        if i_measurement != None:
            x_curr_measurement = x + x_sens*np.cos(theta) - y_sens*np.sin(theta) + measurements[i_measurement]*np.cos(theta+theta_sens)
            y_curr_measurement = y + y_sens*np.cos(theta) + x_sens*np.sin(theta) + measurements[i_measurement]*np.sin(theta+theta_sens)
            for i_height in range(0,np.shape(map)[0]):
                for i_width in range(0,np.shape(map)[1]):
                    if map[i_height][i_width] == 1:
                        #potential need to swap i_height and i_width around
                        curr_dist = np.sqrt((x_curr_measurement - i_height)*(x_curr_measurement - i_height)+(y_curr_measurement-i_width)*(y_curr_measurement-i_width))
                        if curr_dist < dist:
                            dist = curr_dist
            returned_value = returned_value*(z_hit*gaussian_prob(dist,std_hit)+(z_random/z_max))
            
        theta_sens += theta_angle
    return returned_value

def gaussian_prob(dist,stdev):
    #centered at 0
    #may be wrong?
    return 1/(stdev*np.sqrt(2*np.pi))*np.exp(-(dist*dist)/(2*stdev*stdev))
