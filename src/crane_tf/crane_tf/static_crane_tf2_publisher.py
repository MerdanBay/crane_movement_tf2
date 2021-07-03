from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster

from . import tf_transformations

from geometry_msgs.msg import PoseStamped, Point, Quaternion

POSESOURCE='zed2/zed_node'

class FramePublisher(Node):

    def __init__(self):
        super().__init__('crane_tf2_frame_publisher')

        # Declare and acquire `crane` parameter
        self.declare_parameter('machine', 'crane')
        self.cranename = self.get_parameter('machine').get_parameter_value().string_value
        self.crane_front_center_position = Point()
        self.crane_front_center_orientation = Quaternion()
        # Subscribe to a crane{1}{2}/pose topic and call handle_crane_pose
        # callback function on each message
        self.subscription = self.create_subscription(
            PoseStamped,
            f'/{POSESOURCE}/pose',
            self.handle_crane_pose,
            1)
        self.subscription

    def handle_crane_pose(self, msg):
        # Initialize the transform broadcaster
        br = TransformBroadcaster(self)
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'giken'
        t.child_frame_id = self.cranename
        self.crane_front_center_position = msg.pose.position
        self.crane_front_center_orientation = msg.pose.orientation
        
        t.transform.translation.x = self.crane_front_center_position.x
        t.transform.translation.y = self.crane_front_center_position.y
        t.transform.translation.z = 0.0
        # q = tf_transformations.quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = self.crane_front_center_orientation.x
        t.transform.rotation.y = self.crane_front_center_orientation.y
        t.transform.rotation.z = self.crane_front_center_orientation.z
        t.transform.rotation.w = self.crane_front_center_orientation.w

        # print(f"{t.transform.translation.x}:{t.transform.rotation.w}")
        # # Send the transformation
        br.sendTransform(t)


def main():
    rclpy.init()
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()