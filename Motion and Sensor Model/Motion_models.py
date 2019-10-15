import numpy as np

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

    x_center = (x+x_new)/2) + error_free_control(y-y_new)
    y_center = (y+y_new)/2) + error_free_control(x_new-x)
    r_center = np.sqrt((x-x_center)*(x-x_center)+(y-y_center)*(y-y_center))

    angle_change = np.arctan2(y_new-y_center, x_new - x_center) - np.arctan2(y-y_center, x -x_center)

    error_free_trans_vel = angle_change/time * r_center
    error_free_rot_vel = angle_change/time
    rand_term = (theta-theta_new)/time - error_free_rot_vel

    trans_error_prob = prob(trans_vel-error_free_trans_vel, a_1*trans_vel*trans_vel + a_2*rot_vel*rot_vel)
    rot_error_prob = prob(rot_vel-error_free_rot_vel,a_3*trans_vel*trans_vel + a_4*rot_vel*rot_vel)
    rand_term_prob = prob(rand_term, a_5*trans_vel*trans_vel + a_6*rot_vel*rot_vel)

    return trans_error_prob*rot_error_prob*y_with_hat_prob

def prob_norm(argument,variance):
    return 1/np.sqrt(2*np.pi*variance) * exp(-0.5*argument*argument/variance)

def prob_triangle(argument, variance):
    return max(0, (1/(sqrt(6)*np.sqrt(variance)) - abs(argument)/6*variance )
