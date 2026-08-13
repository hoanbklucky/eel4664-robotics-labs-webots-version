#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

UR_JOINTS = [
    'shoulder_pan_joint','shoulder_lift_joint','elbow_joint',
    'wrist_1_joint','wrist_2_joint','wrist_3_joint'
]

class JointStateInspector(Node):
    def __init__(self):
        super().__init__('eel4664_joint_state_inspector')
        self.create_subscription(JointState, '/joint_states', self.callback, 10)
        self.get_logger().info('Listening to /joint_states. Press Ctrl+C to stop.')

    def callback(self, msg):
        lookup = dict(zip(msg.name, msg.position))
        if not all(j in lookup for j in UR_JOINTS):
            return
        line = '  '.join(f'{j}={lookup[j]:+.4f} rad' for j in UR_JOINTS)
        self.get_logger().info(line)

def main():
    rclpy.init(); node = JointStateInspector()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__': main()
