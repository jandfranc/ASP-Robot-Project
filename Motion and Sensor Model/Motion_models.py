import numpy as np
import random
from math import sqrt, sin, cos

def velocity_motion_model(pose, previous_pose,control, time, prob):
    #poses are vectors containing x, y and angular values, respectively
    #control is a vector containing translational velocity and rotational velocity, respectively
    #time is time taken for transition
    #velocity model used for probabilistic motion planning
    #prob is the probability function to use
    x, y, theta = previous_pose
    x_new, y_new, theta_new = pose
    trans_vel, rot_vel = control
    a_1 = 1
    a_2 = 1
    a_3 = 1
    a_4 = 1
    a_5 = 1
    a_6 = 1

    error_free_control_numerator = (x-x_new)*np.cos(rot_vel)+(y-y_new)*np.sin(rot_vel)
    error_free_control_denominator = (x-x_new)*np.cos(rot_vel)-(y-y_new)*np.sin(rot_vel)
    error_free_control = 0.5*error_free_control_numerator/error_free_control_denominator

    x_center = ((x+x_new)/2) + error_free_control(y-y_new)
    y_center = ((y+y_new)/2) + error_free_control(x_new-x)
    r_center = np.sqrt((x-x_center)*(x-x_center)+(y-y_center)*(y-y_center))

    angle_change = np.arctan2(y_new-y_center, x_new - x_center) - np.arctan2(y-y_center, x -x_center)

    error_free_trans_vel = angle_change/time * r_center
    error_free_rot_vel = angle_change/time
    rand_term = (theta-theta_new)/time - error_free_rot_vel

    trans_error_prob = prob(trans_vel-error_free_trans_vel, a_1*trans_vel*trans_vel + a_2*rot_vel*rot_vel)
    rot_error_prob = prob(rot_vel-error_free_rot_vel,a_3*trans_vel*trans_vel + a_4*rot_vel*rot_vel)
    rand_term_prob = prob(rand_term, a_5*trans_vel*trans_vel + a_6*rot_vel*rot_vel)

    return trans_error_prob*rot_error_prob*rand_term_prob

def prob_norm(argument,variance):
    return 1/np.sqrt(2*np.pi*variance) * exp(-0.5*argument*argument/variance)

def prob_triangle(argument, variance):
    return max(0, (1/(sqrt(6)*np.sqrt(variance)) - abs(argument)/6*variance ))


def sample_motion_model_velocity(previous_pose,control,time, sample):

    #poses are vectors containing x, y and angular values, respectively
    #control is a vector containing translational velocity and rotational velocity, respectively
    #time is time taken for transition
    #velocity model used for probabilistic motion planning
    #sample is the probability function to use
    x, y, theta = previous_pose
    trans_vel, rot_vel = control

    a_1 = 1
    a_2 = 1
    a_3 = 1
    a_4 = 1
    a_5 = 1
    a_6 = 1

    trans_error_prob = trans_vel + sample(a_1*trans_vel*trans_vel + a_2*rot_vel*rot_vel)
    rot_error_prob = rot_vel + sample(a_3*trans_vel*trans_vel + a_4*rot_vel*rot_vel)
    rand_term_prob = sample(a_5*trans_vel*trans_vel + a_6*rot_vel*rot_vel)

    x_new = x-(trans_error_prob/rot_error_prob)*sin(theta)+(trans_error_prob/rot_error_prob)*sin(theta+rot_error_prob*time)
    y_new = y+(trans_error_prob/rot_error_prob)*cos(theta)-(trans_error_prob/rot_error_prob)*cos(theta+rot_error_prob*time)
    theta_new = theta+rot_error_prob*time + rand_term_prob*time

    return x_new, y_new, theta_new

def sample_norm(variance):
    sqrt_variance = sqrt(variance)
    sum_list = []
    for i in range(0,12):
        sum_list.append(random.uniform(-sqrt_variance, sqrt_variance))
    return 0.5 * sum(sum_list)

def sample_triangle(variance):
    sqrt_variance = sqrt(variance)
    return (sqrt(6)/2) * (random.uniform(-sqrt_variance, sqrt_variance) + random.uniform(-sqrt_variance, sqrt_variance))


def odom_motion_model(pose,previous_pose,control,prob):
    #poses and control are vectors containing x, y and angular values, respectively
    #time is time taken for transition
    #prob is the probability function to use
    a_1 = 1
    a_2 = 1
    a_3 = 1
    a_4 = 1

    x, y, theta = previous_pose
    x_new, y_new, theta_new = pose
    x_int_new, y_int_new, theta_int_new, x_int, y_int, theta_int =  control

    delta_trans = sqrt((x_int_new-x_int)*(x_int_new-x_int)+(y_int_new-y_int)*(y_int_new-y_int))
    delta_rotone = np.arctan2(y_int_new-y_int,x_int_new-x_int)-theta_int_new
    delta_rottwo = theta_int_new-theta_int-delta_rotone

    delta_hat_trans = sqrt((x-x_new)*(x-x_new)+(y-y_new)*(y-y_new))
    delta_hat_rotone = np.arctan2(y_new-y,x_new-x)-theta_int
    delta_hat_rottwo = theta_new-theta-delta_hat_rotone

    prob_one = prob(delta_trans-delta_hat_trans, a_3*delta_hat_trans*delta_hat_trans+a_4*delta_hat_rotone*delta_hat_rotone+a_4*delta_hat_rottwo*delta_hat_rottwo)
    prob_two = prob(delta_rotone-delta_hat_rotone, a_1*delta_hat_rotone*delta_hat_rotone+a_2*delta_hat_trans*delta_hat_trans)
    prob_three = prob(delta_rottwo-delta_hat_rottwo, a_1*delta_hat_rottwo*delta_hat_rottwo+a_2*delta_hat_trans*delta_hat_trans)

    return prob_one*prob_two*prob_three


def sample_motion_model_odom(previous_pose,control,sample):

    a_1 = 1
    a_2 = 1
    a_3 = 1
    a_4 = 1

    x, y, theta = previous_pose
    x_int_new, y_int_new, theta_int_new, x_int, y_int, theta_int =  control

    delta_trans = sqrt((x_int_new-x_int)*(x_int_new-x_int)+(y_int_new-y_int)*(y_int_new-y_int))
    delta_rotone = np.arctan2(y_int_new-y_int,x_int_new-x_int)-theta_int_new
    delta_rottwo = theta_int_new-theta_int-delta_rotone

    delta_hat_rotone = delta_rotone - sample(a_1*delta_rotone*delta_rotone+a_2*delta_trans*delta_trans)
    delta_hat_trans = delta_trans - sample(a_3*delta_trans*delta_trans+a_4*delta_rotone*delta_rotone+a_4*delta_rottwo*delta_rottwo)
    delta_hat_rottwo = delta_rottwo - sample(a_1*delta_rottwo*delta_rottwo+a_2*delta_trans*delta_trans)

    x_new = x+delta_hat_trans*cos(theta+delta_hat_rotone)
    y_new = y+delta_hat_trans*sin(theta+delta_hat_rotone)
    theta_new = theta + delta_hat_rotone+delta_hat_rottwo

    return x_new, y_new, theta_new

def odom_motion_model(pose,previous_pose,control,prob):
    #poses and control are vectors containing x, y and angular values, respectively
    #time is time taken for transition
    #prob is the probability function to use
    a_1 = 1
    a_2 = 1
    a_3 = 1
    a_4 = 1

    x, y, theta = previous_pose
    x_new, y_new, theta_new = pose
    x_int_new, y_int_new, theta_int_new, x_int, y_int, theta_int =  control

    delta_trans = sqrt((x_int_new-x_int)*(x_int_new-x_int)+(y_int_new-y_int)*(y_int_new-y_int))
    delta_rotone = np.arctan2(y_int_new-y_int,x_int_new-x_int)-theta_int_new
    delta_rottwo = theta_int_new-theta_int-delta_rotone

    delta_hat_trans = sqrt((x-x_new)*(x-x_new)+(y-y_new)*(y-y_new))
    delta_hat_rotone = np.arctan2(y_new-y,x_new-x)-theta_int
    delta_hat_rottwo = theta_new-theta-delta_hat_rotone

    prob_one = prob(delta_trans-delta_hat_trans, a_3*delta_hat_trans*delta_hat_trans+a_4*delta_hat_rotone*delta_hat_rotone+a_4*delta_hat_rottwo*delta_hat_rottwo)
    prob_two = prob(delta_rotone-delta_hat_rotone, a_1*delta_hat_rotone*delta_hat_rotone+a_2*delta_hat_trans*delta_hat_trans)
    prob_three = prob(delta_rottwo-delta_hat_rottwo, a_1*delta_hat_rottwo*delta_hat_rottwo+a_2*delta_hat_trans*delta_hat_trans)

    return prob_one*prob_two*prob_three
