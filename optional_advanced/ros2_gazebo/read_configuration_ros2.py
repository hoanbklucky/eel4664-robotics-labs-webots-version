#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
J=['shoulder_pan_joint','shoulder_lift_joint','elbow_joint','wrist_1_joint','wrist_2_joint','wrist_3_joint']
class OneShot(Node):
    def __init__(self):
        super().__init__('eel4664_read_configuration'); self.done=False
        self.create_subscription(JointState,'/joint_states',self.cb,10)
    def cb(self,msg):
        m=dict(zip(msg.name,msg.position))
        if all(j in m for j in J): print('q =',[m[j] for j in J]); self.done=True

def main():
    rclpy.init(); n=OneShot()
    while rclpy.ok() and not n.done: rclpy.spin_once(n,timeout_sec=1.0)
    n.destroy_node(); rclpy.shutdown()
if __name__=='__main__': main()
