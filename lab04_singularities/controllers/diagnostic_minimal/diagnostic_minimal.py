"""Crash-isolation controller: step Webots without accessing any device."""
from controller import Robot

robot = Robot()
time_step = int(robot.getBasicTimeStep())
print(f"[DIAGNOSTIC PASS] controller started; basicTimeStep={time_step} ms")

steps = 0
while robot.step(time_step) != -1:
    steps += 1
    if steps == 10:
        print("[DIAGNOSTIC PASS] completed 10 steps; world and Python controller are stable")
    if steps >= 100:
        break

print(f"[DIAGNOSTIC DONE] completed {steps} step(s); no motors were commanded")
