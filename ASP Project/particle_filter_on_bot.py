import rospy
from sensor_msgs.msg import LaserScan
import particle_filter as pf
from read_map import map_read
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
import logging

laser_ranges = []
control = []
previous_int_pose = [0,0,0]
def get_data():
    global previous_particles = []
    rospy.Subscriber("base_scan", LaserScan, get_laser)
    rospy.Subscriber("odom", Odometry, get_odom)
    #pub = rospy.Publisher('pose',Pose,queue_size = 100)
    #rospy.init_node('pose_publisher',anonymous = True)
    rate = rospy.Rate(10)

def get_odom(data):
    global control
    control = data.pose.pose

def get_laser(data):
    global laser_ranges
    laser_ranges = data.ranges


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, filename = 'particle.log', filemode = 'w')
    map = map_read('map.jpeg')
    previous_particles = pf.init_particles(map)
    try:
        while not rospy.is_shutdown():
            get_laser_data()
            previous_particles = pf.particle_filter(previous_particles,control,previous_int_pose,laser_ranges,map
            previous_int_pose = control
            logging.info(previous_particles)
    except rospy.ROSInterruptException:
        pass
