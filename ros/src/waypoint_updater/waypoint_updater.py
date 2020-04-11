#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint
from std_msgs.msg import Int32

import numpy as np
import math

from scipy.spatial import KDTree

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 200 # Number of waypoints we will publish. You can change this number
RATE = 40 # Publishing rate for waypoints


class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')

        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below

        rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)


        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)

        # TODO: Add other member variables you need below

        self.waypoints_2d = None
        self.pose = None
        self.base_waypoints = None
        self.waypoint_tree = None

        # rospy.spin()

        self.loop()

    def loop(self):
        pass
        rate = rospy.Rate(RATE)
        while not rospy.is_shutdown():
            if self.pose and self.base_waypoints:
                self.publish_waypoints()
            rate.sleep()

    def get_closest_waypoint_id(self):
        xy = [self.pose.pose.position.x, self.pose.pose.position.x]
        closest_index = self.waypoint_tree.query(xy, 1)[1]

        closest_coord = self.waypoints_2d[closest_index]
        prev_coord = self.waypoints_2d[closest_index-1]

        cl_vect = np.array(closest_coord)
        prev_vect = np.array(prev_coord)
        pos_vect = np.array(xy)

        val = np.dot(cl_vect-prev_vect, pos_vect-cl_vect)

        if val > 0:
            closest_index = (closest_index + 1) % len(self.waypoints_2d)
        return closest_index

    def publish_waypoints(self, closest_index):
        waypoints_lane = Lane()
        waypoints_lane.header = self.base_waypoints.header
        waypoints_lane.waypoints = self.base_waypoints.waypoints[closest+index:closest_index+LOOKAHEAD_WPS]
        self.final_waypoints_pub(waypoints_lane)

    def pose_cb(self, msg):
        # TODO: Implement
        pass

    def waypoints_cb(self, waypoints):
        # TODO: Implement
        pass

    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        self.stopline_wp_idx = msg.data

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
