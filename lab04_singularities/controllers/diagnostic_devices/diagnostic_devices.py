"""List every Webots device without enabling sensors or commanding actuators."""
from controller import Robot

robot = Robot()
time_step = int(robot.getBasicTimeStep())
count = robot.getNumberOfDevices()
print(f"[DEVICE DIAGNOSTIC] robot={robot.getName()!r}; devices={count}")

for index in range(count):
    device = robot.getDeviceByIndex(index)
    print(f"{index:02d}: name={device.getName()!r}; node_type={device.getNodeType()}")

if robot.step(time_step) == -1:
    print("[DEVICE DIAGNOSTIC] simulation ended before one step")
else:
    print("[DIAGNOSTIC PASS] all device handles enumerated; no devices were enabled or commanded")
