#!/usr/bin/env python3
import numpy as np
import rospy
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import tf

last_data = ""
started = False
pub = rospy.Publisher('/chaser_sat_data', PoseStamped, queue_size=1000)

def callback(data):
    # print("New message received")
    global started, last_data
    last_data = data
    if (not started):
        started = True

def timer_callback(event):
    global started, pub, last_data
    if (started):
        current_pose = PoseStamped()
        current_pose.header.frame_id = "chaser_sat_data"
        current_pose.header.stamp = last_data.header.stamp
        current_pose.pose.position.x = last_data.transform.translation.x
        current_pose.pose.position.y = last_data.transform.translation.y
        current_pose.pose.position.z = last_data.transform.translation.z
        current_pose.pose.orientation.x = last_data.transform.rotation.x
        current_pose.pose.orientation.y = last_data.transform.rotation.y
        current_pose.pose.orientation.z = last_data.transform.rotation.z
        current_pose.pose.orientation.w = last_data.transform.rotation.w
        pub.publish(current_pose)
        # print("Last message published")

def listener():
    rospy.init_node('convert_pose_data')
    pose_data = rospy.Subscriber('/vicon/chaser_sat/chaser_sat', TransformStamped, callback)
    timer = rospy.Timer(rospy.Duration(0.01), timer_callback)
    rospy.spin()
    timer.shutdown()

if __name__ == '__main__':
    print("Running")
    listener()
