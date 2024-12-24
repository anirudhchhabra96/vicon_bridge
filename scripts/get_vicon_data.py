#!/usr/bin/env python3
import numpy as np
import rospy
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseStamped, Pose
from std_msgs.msg import String
import tf
import argparse
# Initialize the argument parser
parser = argparse.ArgumentParser(description="A ROS node to convert Vicon object info from TransformStamped to PoseStamped")

# Add an argument for specifying the ROS topic name
# parser.add_argument('--topic', type=str, required=True, help="The name of the ROS topic to publish to.")

# Add arguments for specifying the ROS topic name and the node name
parser.add_argument('--topic', type=str, required=True, help="The name of the ROS topic to publish to.")
# parser.add_argument('--node', type=str, required=True, help="The name of the ROS node.")
args, unknown = parser.parse_known_args()


# Parse the command-line arguments
# args = parser.parse_args()

# Get the topic name from the parsed arguments
# topic_name = args.topic   
topic_name = args.topic
# node_name = args.node


print(topic_name)
last_data = ""
started = False
pub = rospy.Publisher(topic_name.split("/")[2], Pose, queue_size=5)

def callback(data):
    # print("New message received")
    global started, last_data
    last_data = data
    if (not started):
        started = True

def timer_callback(event):
    global started, pub, last_data
    if (started):
        current_pose = Pose()
        # current_pose.header.frame_id = topic_name.split("/")[2]
        # current_pose.header.stamp = last_data.header.stamp
        current_pose.position.x = last_data.transform.translation.x
        current_pose.position.y = last_data.transform.translation.y
        current_pose.position.z = last_data.transform.translation.z
        current_pose.orientation.x = last_data.transform.rotation.x
        current_pose.orientation.y = last_data.transform.rotation.y
        current_pose.orientation.z = last_data.transform.rotation.z
        current_pose.orientation.w = last_data.transform.rotation.w
        pub.publish(current_pose)
        # print("Last message published")

def listener():
    
    rospy.init_node('default_node_name', anonymous=False)
    pose_data = rospy.Subscriber(topic_name, TransformStamped, callback)
    timer = rospy.Timer(rospy.Duration(0.01), timer_callback)
    rospy.spin()
    timer.shutdown()

if __name__ == '__main__':
    print("Running")
    listener()
