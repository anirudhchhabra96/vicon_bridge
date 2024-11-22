#!/usr/bin/env python3
import numpy as np
import rospy
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import tf
import argparse
# Initialize the argument parser
parser = argparse.ArgumentParser(description="A ROS node to convert Vicon object info from TransformStamped to PoseStamped")

# Add an argument for specifying the ROS topic name
parser.add_argument('--topic', type=str, required=True, help="The name of the ROS topic to publish to.")

# Parse the command-line arguments
args = parser.parse_args()

# Get the topic name from the parsed arguments
topic_name = args.topic
print(topic_name)
last_data = ""
started = False
pub = rospy.Publisher(topic_name.split("/")[2], PoseStamped, queue_size=1000)

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
        current_pose.header.frame_id = topic_name.split("/")[2]
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
    pose_data = rospy.Subscriber(topic_name, TransformStamped, callback)
    timer = rospy.Timer(rospy.Duration(0.01), timer_callback)
    rospy.spin()
    timer.shutdown()

if __name__ == '__main__':
    print("Running")
    listener()
