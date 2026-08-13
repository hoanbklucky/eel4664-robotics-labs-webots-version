# Lab 04 — Forward Kinematics of the UR5e

## Learning objectives

- compute FK from a sequence of link transforms;
- implement a DH transform;
- obtain live joint angles from `/joint_states`;
- compare predicted tool pose with TF2;
- quantify position and orientation error.

## Important rule

Do **not** call MoveIt FK or another kinematics solver. TF2 is only the reference after your own FK is computed.

## Part 1 — Planar warm-up

Complete `src/planar_fk.py` for a 3R planar arm and verify two configurations by hand.

## Part 2 — DH transform

Implement `dh_transform(a, alpha, d, theta)` in `src/ur5e_fk_starter.py`.

## Part 3 — UR5e parameters

Enter the six UR5e rows using the exact frame convention and kinematic parameter table supplied in lecture/course notes.

**Do not copy an arbitrary online table without checking the frame convention.**

## Part 4 — Read live joint positions


## Launch the simulator

Terminal 1:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e
```

Leave this terminal running. Use a second terminal for commands and your code.


```bash
python3 lab04_forward_kinematics/src/read_configuration.py
```

Save three different configurations.

## Part 5 — Compute FK

For each configuration calculate the full transform chain and record predicted position/orientation.

## Part 6 — Obtain TF reference

```bash
ros2 run tf2_ros tf2_echo <base_frame> <tool_frame>
```

Use frames consistent with your FK convention. Document any fixed terminal transform you apply.

## Part 7 — Quantify error

Position:

```text
||p_FK - p_TF||
```

Orientation:

```text
R_err = R_FK^T R_TF
```

Report the equivalent rotation-angle error.

## Questions

1. What inputs are required by FK?
2. Why can correct FK implementations use different matrices for the same physical pose?
3. What is the role of a fixed tool/flange transform?
4. Why is comparing XYZ alone insufficient?
5. How would a joint-sign error appear in your results?
