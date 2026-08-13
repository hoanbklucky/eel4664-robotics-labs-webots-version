#!/usr/bin/env python3
import argparse, rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener

class Query(Node):
    def __init__(self, target, source):
        super().__init__('eel4664_tf_query')
        self.target=target; self.source=source
        self.buffer=Buffer(); self.listener=TransformListener(self.buffer,self)
        self.timer=self.create_timer(0.5,self.tick)
    def tick(self):
        try:
            t=self.buffer.lookup_transform(self.target,self.source,rclpy.time.Time())
        except Exception as e:
            self.get_logger().info(f'Waiting for transform: {e}'); return
        tr=t.transform.translation; q=t.transform.rotation
        print(f'{self.target} <- {self.source}')
        print(f'translation = [{tr.x:.6f}, {tr.y:.6f}, {tr.z:.6f}] m')
        print(f'quaternion  = [{q.x:.6f}, {q.y:.6f}, {q.z:.6f}, {q.w:.6f}]')
        raise SystemExit

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--target',default='base_link'); ap.add_argument('--source',default='tool0')
    a=ap.parse_args(); rclpy.init(); n=Query(a.target,a.source)
    try: rclpy.spin(n)
    except SystemExit: pass
    finally: n.destroy_node(); rclpy.shutdown()
if __name__=='__main__': main()
