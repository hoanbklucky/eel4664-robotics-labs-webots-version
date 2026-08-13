#!/usr/bin/env python3
import argparse
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

JOINTS = [
    'shoulder_pan_joint','shoulder_lift_joint','elbow_joint',
    'wrist_1_joint','wrist_2_joint','wrist_3_joint'
]

class GoalSender(Node):
    def __init__(self):
        super().__init__('eel4664_joint_goal_sender')
        self.client = ActionClient(self, FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory')

    def send(self, positions, duration):
        self.get_logger().info('Waiting for joint trajectory controller...')
        self.client.wait_for_server()
        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = JOINTS
        point = JointTrajectoryPoint()
        point.positions = list(positions)
        point.time_from_start.sec = int(duration)
        point.time_from_start.nanosec = int((duration-int(duration))*1e9)
        goal.trajectory.points = [point]
        future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        handle = future.result()
        if not handle.accepted:
            raise RuntimeError('Trajectory goal was rejected.')
        self.get_logger().info('Goal accepted; waiting for result...')
        rf = handle.get_result_async(); rclpy.spin_until_future_complete(self, rf)
        self.get_logger().info(f'Finished with error_code={rf.result().result.error_code}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--positions', nargs=6, type=float,
                    default=[0.0,-1.2,1.2,-1.5,-1.57,0.0])
    ap.add_argument('--duration', type=float, default=5.0)
    a=ap.parse_args(); rclpy.init(); n=GoalSender()
    try: n.send(a.positions,a.duration)
    finally: n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
